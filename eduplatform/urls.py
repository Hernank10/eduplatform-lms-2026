from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views as edu_views


urlpatterns = [
    path('', edu_views.home, name='home'),
    path('dashboard/', edu_views.dashboard_redirect, name='dashboard'),

    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),

    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('accounts.urls')),  # ← FALTA ESTA LÍNEA

    path('courses/', include('courses.urls')),
    path('assessments/', include('assessments.urls')),
    path('gamification/', include('gamification.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)