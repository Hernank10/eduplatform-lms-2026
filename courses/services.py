from courses.models import Lesson, Progress


def course_progress_percent(student, course):
    total = Lesson.objects.filter(course=course).count()

    if total == 0:
        return 0

    completed = Progress.objects.filter(
        student=student,
        lesson__course=course,
        status="completed"
    ).count()

    return int((completed / total) * 100)

