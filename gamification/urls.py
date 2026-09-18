from django.urls import path
from . import views

app_name = 'gamification'

urlpatterns = [
    path('ranking/', views.leaderboard, name='leaderboard'),
    path('logros/', views.achievements, name='achievements'),
    path('certificados/', views.certificates, name='certificates'),
    path('certificados/<str:code>/', views.certificate_detail, name='certificate_detail'),
    path('desafio/', views.challenge_today, name='challenge_today'),
]
