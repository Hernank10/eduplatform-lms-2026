from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
import pytz

# 1. Tu modelo de Usuario ya existente (con los campos de rol)
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        return self.username

# 2. El nuevo Perfil para la multiculturalidad (Idioma y Zona Horaria)
class Profile(models.Model):
    # Aquí usamos 'accounts.User' para referirnos a tu modelo personalizado
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='profile')
    
    LANGUAGES = [
        ('es', _('Español')),
        ('en', _('Inglés')),
    ]
    language = models.CharField(max_length=10, choices=LANGUAGES, default='es')
    
    TIMEZONES = [(tz, tz) for tz in pytz.all_timezones]
    timezone = models.CharField(max_length=100, choices=TIMEZONES, default='UTC')

    def __str__(self):
        return f"Perfil de {self.user.username}"

# 3. SEÑALES automáticas
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Usamos hasattr para evitar errores si el perfil no existe por alguna razón
    if hasattr(instance, 'profile'):
        instance.profile.save()
