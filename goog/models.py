from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class SubjectInfo(models.Model):
    student = models.OneToOneField(User)

    class Meta:
        app_label = 'goog'


class Search(models.Model):
    student = models.ForeignKey(User)
    search_term = models.CharField(max_length=200, default='')
    search_engine_choice = models.IntegerField(default=None, null=True)
    search_url = models.CharField(max_length=1000)
    search_timestamp = models.DateTimeField(default=None, null=True)
    next_action_timestamp = models.DateTimeField(default=None, null=True)
    duration_setting = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    class Meta:
        app_label = 'goog'


class Duration(models.Model):
    global_duration = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    search_engine_choice = models.IntegerField(default=1)
