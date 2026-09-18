from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from courses.models import Course, Lesson, Enrollment
from .models import Assessment, Question, Choice, Submission


@login_required
def assessment_list(request, course_pk):
    """Lista de evaluaciones de un curso."""
    curso = get_object_or_404(Course, pk=course_pk)
    evaluaciones = curso.assessments.all()
    return render(request, 'assessments/assessment_list.html', {
        'curso': curso,
        'evaluaciones': evaluaciones,
    })


@login_required
def assessment_take(request, pk):
    """Tomar una evaluacion."""
    evaluacion = get_object_or_404(Assessment, pk=pk)
    curso = evaluacion.course

    # Verificar inscripcion
    inscrito = Enrollment.objects.filter(
        student=request.user, course=curso
    ).exists()

    if not inscrito and not request.user.is_staff:
        messages.warning(request, 'Debes inscribirte en el curso primero')
        return redirect('course_detail', pk=curso.pk)

    preguntas = evaluacion.questions.all().prefetch_related('choices')

    if request.method == 'POST':
        # Calcular puntuacion
        total_puntos = 0
        puntos_obtenidos = 0

        for pregunta in preguntas:
            total_puntos += pregunta.points
            respuesta = request.POST.get('pregunta_' + str(pregunta.id), '')

            if pregunta.question_type == 'mcq' or pregunta.question_type == 'true_false':
                # Buscar la opcion correcta
                try:
                    choice = pregunta.choices.get(id=respuesta)
                    if choice.is_correct:
                        puntos_obtenidos += pregunta.points
                except (Choice.DoesNotExist, ValueError):
                    pass
            else:
                # Respuesta corta/abierta: guardar como submission para revision
                pass

        # Calcular nota (0-100)
        if total_puntos > 0:
            nota = (puntos_obtenidos / total_puntos) * 100
        else:
            nota = 0

        # Crear submission
        submission = Submission.objects.create(
            student=request.user,
            assessment=evaluacion,
            grade=nota,
            is_graded=True,
            transcription='Evaluacion completada en linea',
        )

        # Actualizar progreso del curso
        try:
            enrollment = Enrollment.objects.get(student=request.user, course=curso)
            total_lecciones = curso.lessons.count()
            completadas = 0
            if total_lecciones > 0:
                enrollment.progress = min(100, int((nota / 100) * 100))
                enrollment.save()
        except Enrollment.DoesNotExist:
            pass

        messages.success(request, 'Evaluacion completada. Nota: ' + str(round(nota, 2)) + '/100')
        return redirect('assessment_result', pk=submission.pk)

    return render(request, 'assessments/take_assessment.html', {
        'evaluacion': evaluacion,
        'curso': curso,
        'preguntas': preguntas,
    })


@login_required
def assessment_result(request, pk):
    """Ver el resultado de una evaluacion."""
    submission = get_object_or_404(Submission, pk=pk)

    if submission.student != request.user and not request.user.is_staff:
        messages.error(request, 'No tienes acceso a este resultado')
        return redirect('home')

    return render(request, 'assessments/result.html', {
        'submission': submission,
        'evaluacion': submission.assessment,
    })


@login_required
def assessment_history(request):
    """Historial de evaluaciones del usuario."""
    submissions = Submission.objects.filter(
        student=request.user
    ).select_related('assessment', 'assessment__course').order_by('-submitted_at')

    return render(request, 'assessments/history.html', {
        'submissions': submissions,
    })
