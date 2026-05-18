from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("add/", views.add_work_log, name="add_work_log"),
]