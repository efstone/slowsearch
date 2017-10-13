from django.contrib import admin
from goog.models import *

# Register your models here.

class DurationAdmin(admin.ModelAdmin):
    fields = ['global_duration']
    list_display = ['global_duration']


class SearchAdmin(admin.ModelAdmin):
    fields = ['student', 'search_term', 'search_url', 'search_timestamp', 'next_action_timestamp', 'duration_setting']
    list_display = ['student', 'search_term', 'search_url', 'search_timestamp', 'next_action_timestamp', 'duration_setting']


admin.site.register(Duration, DurationAdmin)
admin.site.register(Search, SearchAdmin)