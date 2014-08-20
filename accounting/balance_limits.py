import abc
import pickle
from django.core.exceptions import ObjectDoesNotExist
from horizon.utils import memoized
from accounting.models import Threshold
from accounting.models import PassedThreshold


class ThresholdAction(object):

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


class BalanceLimits(object):

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
                ThresholdAction.get_subclass_of_name(
                    action).handler(passed_limit=threshold.balance,
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
