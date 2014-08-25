from django.db import models


class Threshold(models.Model):
    balance = models.DecimalField(max_digits=19, decimal_places=10)
    actions = models.TextField(blank=True)
    up = models.BooleanField(default=False)
    down = models.BooleanField(default=False)


class PassedThreshold(models.Model):
    project_id = models.CharField(max_length=64)
    threshold = models.ForeignKey(Threshold)
    datetime = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('project_id', 'threshold'),)


class ActionQueue(models.Model):
    verbose_name = models.CharField(max_length=64)
    due_datetime = models.DateTimeField(db_index=True)
    kwargs = models.TextField(blank=True)
    processed = models.BooleanField(default=False)
