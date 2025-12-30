from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Enrollment, Progress


@login_required
def student_dashboard(request):
    user = request.user

    enrollments = Enrollment.objects.filter(student=user).select_related("course")

    progress_data = []
    for enrollment in enrollments:
        course = enrollment.course
        lessons_progress = Progress.objects.filter(
            student=user, lesson__course=course
        )

        total = lessons_progress.count()
        completed = lessons_progress.filter(status="completed").count()

        percent = int((completed / total) * 100) if total > 0 else 0

        progress_data.append(
            {
                "course": course,
                "percent": percent,
                "completed": completed,
                "total": total,
            }
        )

    return render(
        request,
        "courses/student_dashboard.html",
        {
            "progress_data": progress_data
        }
    )

