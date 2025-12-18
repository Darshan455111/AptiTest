from django.shortcuts import render
from .models import Question

def test_view(request):
    questions = Question.objects.all()
    total_questions = questions.count()
    time_limit = total_questions * 60  # seconds

    if request.method == "POST":
        score = 0
        for q in questions:
            selected = request.POST.get(str(q.id))
            if selected:
                if q.option_set.filter(id=selected, is_correct=True).exists():
                    score += 1

        return render(request, "testapp/result.html", {
            "score": score,
            "total": total_questions
        })

    return render(request, "testapp/test.html", {
        "questions": questions,
        "time_limit": time_limit
    })
