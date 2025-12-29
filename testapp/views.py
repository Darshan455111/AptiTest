from django.shortcuts import render
from .models import Question
import random


def test_view(request):
    # ---------------------------
    # GET REQUEST → SHOW TEST
    # ---------------------------
    if request.method == "GET":
        questions = list(Question.objects.all())

        # Randomize questions
        random.shuffle(questions)

        # Optional limit (change if needed)
        questions = questions[:10]

        # Save question IDs in session (CRITICAL FIX)
        request.session["question_ids"] = [q.id for q in questions]

        total_questions = len(questions)
        time_limit = total_questions * 60  # 1 min per question

        return render(request, "testapp/test.html", {
            "questions": questions,
            "time_limit": time_limit
        })

    # ---------------------------
    # POST REQUEST → PROCESS RESULT
    # ---------------------------
    if request.method == "POST":
        question_ids = request.session.get("question_ids", [])
        questions = Question.objects.filter(id__in=question_ids)

        score = 0
        review_data = []

        for q in questions:
            selected_option_id = request.POST.get(str(q.id))
            correct_option = q.option_set.get(is_correct=True)

            is_correct = (
                selected_option_id and
                int(selected_option_id) == correct_option.id
            )

            if is_correct:
                score += 1

            review_data.append({
                "question": q,
                "options": q.option_set.all(),
                "selected_option_id": int(selected_option_id) if selected_option_id else None,
                "correct_option_id": correct_option.id
            })

        total_questions = len(questions)
        percentage = int((score / total_questions) * 100) if total_questions else 0

        return render(request, "testapp/result.html", {
            "score": score,
            "total": total_questions,
            "percentage": percentage,
            "review_data": review_data
        })
