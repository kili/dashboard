from django.db import models


class Threshold(models.Model):
    balance = models.IntegerField(unique=True)
    actions = models.TextField(blank=True)
    up = models.BooleanField(default=False)
    down = models.BooleanField(default=False)


class PassedThreshold(models.Model):
    project_id = models.CharField(max_length=64)
    threshold = models.ForeignKey(Threshold)
    datetime = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('project_id', 'threshold'),)
