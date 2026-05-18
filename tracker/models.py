from django.db import models
from django.contrib.auth.models import User


class WorkLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    work_date = models.DateField()

    hours = models.PositiveIntegerField(default=0)
    minutes = models.PositiveIntegerField(default=0)

    note = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-work_date", "-created_at"]

    def total_minutes(self):
        return self.hours * 60 + self.minutes

    def __str__(self):
        return f"{self.user.username} - {self.work_date}"