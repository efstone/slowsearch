from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class SubjectInfo(models.Model):
    student = models.OneToOneField(User)

    class Meta:
        app_label = 'goog'

class Search(models.Model):
    search_term = models.CharField(max_length=200, default='')
    search_timestamp = models.DateTimeField(default=0)
    next_action_timestamp = models.DateTimeField(default=0)
    duration_setting = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    class Meta:
        app_label = 'goog'
