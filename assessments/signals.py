from django.db.models.signals import post_save
from django.dispatch import receiver
from courses.models import Progress, Lesson
from .models import Submission

@receiver(post_save, sender=Submission)
def handle_submission_logic(sender, instance, created, **kwargs):
    # Evitamos bucles infinitos al guardar
    if kwargs.get('update_fields') and 'is_graded' in kwargs.get('update_fields'):
        return

    # 1. EVALUACIÓN (¿Aprobó o no?)
    # Para Quizzes automáticos: se puede definir una lógica de puntos.
    # Para Caligrafía: esperamos tu nota manual en 'grade'.
    
    threshold = 70.0 # Umbral de aprobación
    
    if instance.grade is not None:
        passed = instance.grade >= threshold
        
        # Solo actualizamos si el estado de aprobación cambió
        if instance.is_graded != passed:
            # Usamos update para no disparar esta señal otra vez
            Submission.objects.filter(pk=instance.pk).update(is_graded=passed)
            # Actualizamos la instancia en memoria para que el resto del código lo sepa
            instance.is_graded = passed

    # 2. PROGRESO Y DESBLOQUEO (Solo si ya está calificado y aprobado)
    if instance.is_graded and instance.assessment.lesson:
        student = instance.student
        lesson = instance.assessment.lesson
        course = lesson.course

        # Marcar lección actual como completada
        # (Asegúrate de que el modelo Progress use 'user' o 'student')
        Progress.objects.update_or_create(
            user=student, 
            lesson=lesson,
            defaults={'is_completed': True}
        )

        # Buscar y desbloquear la siguiente lección
        next_lesson = Lesson.objects.filter(
            course=course,
            order__gt=lesson.order
        ).order_by('order').first()

        if next_lesson:
            Progress.objects.get_or_create(user=student, lesson=next_lesson)
