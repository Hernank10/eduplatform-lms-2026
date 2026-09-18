from django.urls import path
from . import views

app_name = 'assessments'

urlpatterns = [
    path('', views.assessment_history, name='history'),
    path('curso/<int:course_pk>/', views.assessment_list, name='list'),
    path('<int:pk>/', views.assessment_take, name='take'),
    path('resultado/<int:pk>/', views.assessment_result, name='result'),
]
