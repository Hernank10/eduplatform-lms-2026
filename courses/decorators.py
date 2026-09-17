from functools import wraps
from django.shortcuts import redirect, get_object_or_404

from courses.models import Progress


def lesson_unlocked(view_func):
    """
    Permite acceder a una vista SOLO si la lección
    está desbloqueada (status = in_progress).
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        assessment_id = kwargs.get("assessment_id")

        # Import local para evitar ciclos
        from assessments.models import Assessment

        assessment = get_object_or_404(Assessment, id=assessment_id)
        lesson = assessment.lesson

        progress = Progress.objects.filter(
            student=request.user,
            lesson=lesson
        ).first()

        if not progress or progress.status != "in_progress":
            # 🔑 nombre CORRECTO de la URL
            return redirect("courses:student_dashboard")

        return view_func(request, *args, **kwargs)

    return _wrapped_view

