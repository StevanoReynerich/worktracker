from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import WorkLogForm
from .models import WorkLog


LIMIT_MINUTES = 48 * 60


@login_required
def dashboard(request):
    today = timezone.localdate()
    start_date = today - timedelta(days=13)

    logs = WorkLog.objects.filter(
        user=request.user,
        work_date__range=[start_date, today]
    )

    used_minutes = sum(log.total_minutes() for log in logs)
    left_minutes = max(LIMIT_MINUTES - used_minutes, 0)

    calendar_days = []

    for i in range(14):
        day = start_date + timedelta(days=i)
        day_logs = logs.filter(work_date=day)

        total_minutes = sum(log.total_minutes() for log in day_logs)

        calendar_days.append({
            "date": day,
            "date_key": day.strftime("%Y-%m-%d"),
            "day_name": day.strftime("%a"),
            "day_number": day.day,
            "hours": total_minutes // 60,
            "minutes": total_minutes % 60,
            "has_work": total_minutes > 0,
            "logs": day_logs,
        })

    context = {
        "logs": logs,
        "calendar_days": calendar_days,
        "used_hours": used_minutes // 60,
        "used_minutes": used_minutes % 60,
        "left_hours": left_minutes // 60,
        "left_minutes": left_minutes % 60,
        "percent_used": min(round((used_minutes / LIMIT_MINUTES) * 100), 100),
    }

    return render(request, "tracker/dashboard.html", context)


@login_required
def add_work_log(request):
    if request.method == "POST":
        form = WorkLogForm(request.POST)

        if form.is_valid():
            work_log = form.save(commit=False)
            work_log.user = request.user
            work_log.save()
            messages.success(request, "Work log added.")
            return redirect("dashboard")
    else:
        form = WorkLogForm(initial={"work_date": timezone.localdate()})

    return render(request, "tracker/add_work_log.html", {
        "form": form,
        "is_edit": False,
    })


@login_required
def edit_work_log(request, log_id):
    work_log = get_object_or_404(
        WorkLog,
        id=log_id,
        user=request.user
    )

    if request.method == "POST":
        form = WorkLogForm(request.POST, instance=work_log)

        if form.is_valid():
            form.save()
            messages.success(request, "Work log updated.")
            return redirect("dashboard")
    else:
        form = WorkLogForm(instance=work_log)

    return render(request, "tracker/add_work_log.html", {
        "form": form,
        "is_edit": True,
    })


@login_required
def delete_work_log(request, log_id):
    work_log = get_object_or_404(
        WorkLog,
        id=log_id,
        user=request.user
    )

    if request.method == "POST":
        work_log.delete()
        messages.success(request, "Work log deleted.")

    return redirect("dashboard")