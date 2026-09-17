from django.urls import path
from . import views

urlpatterns = [
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("teacher/dashboard/", views.teacher_dashboard, name="teacher_dashboard"),
    path("recursos/", views.resource_list, name="resource_list"),
    path("recursos/<int:pk>/", views.resource_detail, name="resource_detail"),
]