from django.shortcuts import render
from .models import Question


def test_view(request):
    # Fetch all questions
    questions = Question.objects.all()
    total_questions = questions.count()

    # Time limit: 1 minute per question
    time_limit = total_questions * 60  # seconds

    # If form submitted (manual or auto)
    if request.method == "POST":
        score = 0

        for question in questions:
            selected_option_id = request.POST.get(str(question.id))

            if selected_option_id:
                # Check if selected option is correct
                if question.option_set.filter(
                        id=selected_option_id,
                        is_correct=True
                ).exists():
                    score += 1

        # Calculate percentage safely
        percentage = int((score / total_questions) * 100) if total_questions > 0 else 0

        return render(
            request,
            "testapp/result.html",
            {
                "score": score,
                "total": total_questions,
                "percentage": percentage
            }
        )

    # Initial test page load
    return render(
        request,
        "testapp/test.html",
        {
            "questions": questions,
            "time_limit": time_limit
        }
    )
