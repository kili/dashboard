import abc
from sets import Set
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
        actions = Set()
        for threshold in cls._get_thresholds():
            if (threshold.up
                    and kwargs['balance_before'] < threshold.balance
                    and kwargs['balance_after'] >= threshold.balance):
                actions.add(threshold)
            if (threshold.down
                    and kwargs['balance_before'] < threshold.balance
                    and kwargs['balance_after'] >= threshold.balance):
                actions.add(threshold)
        for action in actions:
            cls.remember_passing(threshold, kwargs['project_id'])
            ThresholdAction.get_subclass_of_name(
                threshold.action).handler(**kwargs)

    @classmethod
    def remember_passing(cls, threshold, project_id):
        try:
            PassedThreshold.objects.get(project_id=project_id,
                                        threshold=threshold).save()
        except ObjectDoesNotExist:
            PassedThreshold.objects.create(
                project_id=project_id,
                threshold=threshold)
