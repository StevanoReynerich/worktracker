from django.contrib import admin
from .models import WorkLog


@admin.register(WorkLog)
class WorkLogAdmin(admin.ModelAdmin):
    list_display = ("user", "work_date", "hours", "minutes", "note", "created_at")
    list_filter = ("work_date", "user")
    search_fields = ("user__username", "note")