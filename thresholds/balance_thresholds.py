import abc
import pickle
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from horizon.utils import memoized
from thresholds.models import Threshold
from thresholds.models import PassedThreshold
from thresholds.models import ActionQueue


class ThresholdAction(object):
    delay = 0

    @abc.abstractproperty
    def verbose_name():
        pass

    @abc.abstractmethod
    def handler():
        """will get the following kwargs passed:
           passed_limit, project_id, current_balance
        """
        pass

    @classmethod
    def get_subclass_of_name(cls, name):
        for subclass in cls.__subclasses__():
            if subclass.verbose_name == name:
                return subclass
        raise Exception('requested subclass was not found')

    @classmethod
    def queue_for_later(cls, **kwargs):
        ActionQueue.objects.create(
            verbose_name=cls.verbose_name,
            due_datetime=timezone.now() + timezone.delta(seconds=cls.delay),
            kwargs=pickle.dumps(kwargs))

    @classmethod
    def pass_event(cls, **kwargs):
        if cls.delay == 0:
            cls.handler(**kwargs)
        else:
            cls.queue_for_later(**kwargs)


class BalanceThresholds(object):

    @classmethod
    @memoized.memoized_method
    def _get_thresholds(cls):
        return Threshold.objects.all()

    @classmethod
    def process_transaction(cls, **kwargs):
        passed_thresholds = set()
        for threshold in cls._get_thresholds():
            if (threshold.up and
                    kwargs['balance_before'] < threshold.balance and
                    kwargs['balance_after'] >= threshold.balance) or (
                    threshold.down and
                    kwargs['balance_before'] > threshold.balance and
                    kwargs['balance_after'] <= threshold.balance):
                passed_thresholds.add(threshold)
        for threshold in passed_thresholds:
            cls.remember_passing(threshold, kwargs['project_id'])
            for action in pickle.loads(threshold.actions):
                ThresholdAction.get_subclass_of_name(action).pass_event(
                    passed_limit=threshold.balance,
                    project_id=kwargs['project_id'],
                    current_balance=kwargs['balance_after'])

    @classmethod
    def remember_passing(cls, threshold, project_id):
        try:
            PassedThreshold.objects.get(project_id=project_id,
                                        threshold=threshold).save()
        except ObjectDoesNotExist:
            PassedThreshold.objects.create(
                project_id=project_id,
                threshold=threshold)
