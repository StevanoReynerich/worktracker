from django import forms
from .models import WorkLog


class WorkLogForm(forms.ModelForm):
    class Meta:
        model = WorkLog
        fields = ["work_date", "hours", "minutes", "note"]
        widgets = {
            "work_date": forms.DateInput(attrs={"type": "date"}),
            "note": forms.Textarea(attrs={"rows": 3}),
        }