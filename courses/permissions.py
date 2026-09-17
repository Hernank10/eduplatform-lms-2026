from django.core.exceptions import PermissionDenied
from .models import Lesson

def lesson_access_required(view_func):
    def _wrapped_view(request, lesson_id, *args, **kwargs):
        lesson = Lesson.objects.get(id=lesson_id)

        if not lesson.is_unlocked_for(request.user):
            raise PermissionDenied("Lección bloqueada")

        return view_func(request, lesson_id, *args, **kwargs)

    return _wrapped_view

