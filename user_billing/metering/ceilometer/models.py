from django.db import models


class CeilometerFetcherPosition(models.Model):

    meter_name = models.CharField(max_length=64, primary_key=True)
    position = models.DateTimeField()

    class Meta:
        db_table = 'ceilometer_fetcher_position'
