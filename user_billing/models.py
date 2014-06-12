from django.db import models
from user_billing import managers


class RawStatisticsIndex(models.Model):

    year = models.IntegerField()
    month = models.IntegerField()
    meter = models.CharField(max_length=64)
    user_id = models.CharField(max_length=64)
    fetched = models.BooleanField(default=False, db_index=True)
    billed = models.BooleanField(default=False, db_index=True)
    has_data = models.BooleanField(default=False, db_index=True)

    class Meta:
        db_table = 'user_billing_raw_statistics_index'
        index_together = [['user_id',
                           'month',
                           'meter',
                           'year']]
        unique_together = index_together


class RawStatistics(models.Model):

    insert_time = models.DateTimeField(auto_now_add=True)
    data = models.TextField()
    statistics_index = models.OneToOneField(RawStatisticsIndex)

    objects = managers.RawDataManager()

    class Meta:
        db_table = 'user_billing_raw_statistics'
