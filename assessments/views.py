from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from courses.decorators import lesson_unlocked
from .models import Assessment, Question, Choice, Submission


@login_required
@lesson_unlocked
def take_assessment(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    questions = assessment.questions.prefetch_related("choices")

    if request.method == "POST":
        total_points = 0
        obtained_points = 0

        for question in questions:
            total_points += question.points
            answer_key = f"question_{question.id}"
            selected_choice_id = request.POST.get(answer_key)

            if not selected_choice_id:
                continue

            try:
                choice = Choice.objects.get(id=selected_choice_id)
                if choice.is_correct:
                    obtained_points += question.points
            except Choice.DoesNotExist:
                pass

        score = (obtained_points / total_points) * 100 if total_points > 0 else 0
        passed = score >= assessment.passing_score

        Submission.objects.create(
            user=request.user,
            assessment=assessment,
            score=score,
            passed=passed,
        )

        return render(
            request,
            "assessments/result.html",
            {
                "assessment": assessment,
                "score": round(score, 2),
                "passed": passed,
            }
        )

    return render(
        request,
        "assessments/take_assessment.html",
        {
            "assessment": assessment,
            "questions": questions,
        }
    )

