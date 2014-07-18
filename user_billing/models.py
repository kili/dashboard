from django.db import models


class RawStatisticsIndex(models.Model):

    from_ts = models.DateTimeField()
    until_ts = models.DateTimeField()
    meter = models.CharField(max_length=64)
    project_id = models.CharField(max_length=64)
    fetched = models.BooleanField(default=False, db_index=True)
    billed = models.BooleanField(default=False, db_index=True)
    has_data = models.BooleanField(default=False, db_index=True)

    class Meta:
        db_table = 'project_billing_raw_statistics_index'
        unique_together = [['from_ts',
                           'until_ts',
                           'project_id',
                           'meter']]


class RawStatistics(models.Model):

    insert_time = models.DateTimeField(auto_now_add=True)
    data = models.TextField()
    statistics_index = models.ForeignKey(RawStatisticsIndex)

    class Meta:
        db_table = 'project_billing_raw_statistics'
