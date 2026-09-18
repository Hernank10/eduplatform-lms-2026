from django.urls import path
from . import views

urlpatterns = [
    # Dashboards
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("teacher/dashboard/", views.teacher_dashboard, name="teacher_dashboard"),

    # Cursos
    path("", views.course_list, name="course_list"),
    path("<int:pk>/", views.course_detail, name="course_detail"),
    path("<int:pk>/inscribir/", views.course_enroll, name="course_enroll"),

    # Lecciones
    path("leccion/<int:pk>/", views.lesson_detail, name="lesson_detail"),
    path("leccion/<int:pk>/completar/", views.lesson_complete, name="lesson_complete"),

    # Recursos
    path("recursos/", views.resource_list, name="resource_list"),
    path("recursos/<int:pk>/", views.resource_detail, name="resource_detail"),
]
