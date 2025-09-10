from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Quiz, Question, Choice

# 1. List all quizzes
def quiz_list(request):
    quizzes = Quiz.objects.all()  # Get all quizzes from database
    return render(request, 'quizzes/quiz_list.html', {'quizzes': quizzes})

# 2. Show quiz details
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)  # Get quiz or 404 error
    questions = quiz.questions.all()  # Get all questions for this quiz
    return render(request, 'quizzes/quiz_detail.html', {
        'quiz': quiz,
        'questions': questions
    })

# 3. Take the quiz (with randomized choices!)
def take_quiz(request, quiz_id):
    import random
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.questions.all()
    
    # Randomize choices for each question
    for question in questions:
        choices = list(question.choices.all())
        random.shuffle(choices)  # This is where you randomize!
        question.shuffled_choices = choices
    
    return render(request, 'quizzes/take_quiz.html', {
        'quiz': quiz,
        'questions': questions
    })

# 4. Show quiz results (placeholder for now)
def quiz_results(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    return render(request, 'quizzes/results.html', {'quiz': quiz})
