from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from courses.models import Progress, Enrollment
from .models import Achievement, UserAchievement, UserPoints

User = get_user_model()


def otorgar_logro(user, codigo):
    try:
        achievement = Achievement.objects.get(codigo=codigo)
        ua, created = UserAchievement.objects.get_or_create(user=user, achievement=achievement)
        if created:
            puntos, _ = UserPoints.objects.get_or_create(user=user)
            puntos.add_points(achievement.puntos)
            return True
    except Achievement.DoesNotExist:
        pass
    return False


@receiver(post_save, sender=User)
def crear_puntos_usuario(sender, instance, created, **kwargs):
    if created:
        UserPoints.objects.get_or_create(user=instance)


@receiver(post_save, sender=Progress)
def verificar_logros_progreso(sender, instance, created, **kwargs):
    if instance.status != 'completed':
        return
    user = instance.student
    total = Progress.objects.filter(student=user, status='completed').count()
    if total == 1:
        otorgar_logro(user, 'first_lesson')
    if total >= 10:
        otorgar_logro(user, 'ten_lessons')
    if total >= 50:
        otorgar_logro(user, 'fifty_lessons')


@receiver(post_save, sender=Enrollment)
def verificar_logros_inscripcion(sender, instance, created, **kwargs):
    if not created:
        return
    user = instance.student
    total = Enrollment.objects.filter(student=user).count()
    if total >= 5:
        otorgar_logro(user, 'five_courses')
