from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("add/", views.add_work_log, name="add_work_log"),
    path("edit/<int:log_id>/", views.edit_work_log, name="edit_work_log"),
    path("delete/<int:log_id>/", views.delete_work_log, name="delete_work_log"),
]