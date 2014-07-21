from django.db import models


class RawStatisticsIndex(models.Model):

    from_ts = models.DateTimeField(blank=False)
    until_ts = models.DateTimeField(blank=False)
    meter = models.CharField(max_length=64)
    project_id = models.CharField(max_length=64)
    fetched = models.BooleanField(default=False)
    billed = models.BooleanField(default=False)
    has_data = models.BooleanField(default=False)

    class Meta:
        unique_together = [['from_ts',
                            'until_ts',
                            'project_id',
                            'meter']]


class RawStatistics(models.Model):

    insert_time = models.DateTimeField(auto_now_add=True)
    data = models.TextField()
    statistics_index = models.ForeignKey(RawStatisticsIndex)
