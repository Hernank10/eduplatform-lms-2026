from django.urls import path
from . import views

app_name = "assessments"

urlpatterns = [
    path("<int:assessment_id>/take/", views.take_assessment, name="take"),
]

