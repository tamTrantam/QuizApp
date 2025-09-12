from django.shortcuts import render, get_object_or_404, redirect
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
    
    if request.method == 'POST':
        # Process quiz submission and track votes
        score = 0
        total_questions = quiz.questions.count()
        
        for question in quiz.questions.all():
            selected_choice_id = request.POST.get(f'question_{question.id}')
            if selected_choice_id:
                try:
                    selected_choice = Choice.objects.get(id=selected_choice_id)
                    # Increment vote count for analytics
                    selected_choice.votes += 1
                    selected_choice.save()
                    
                    # Check if answer is correct
                    if selected_choice.is_correct:
                        score += 1
                except Choice.DoesNotExist:
                    pass
        
        # Calculate percentage score
        percentage_score = (score / total_questions * 100) if total_questions > 0 else 0
        
        # Store results in session for results page
        request.session['quiz_results'] = {
            'quiz_id': quiz.id,
            'score': score,
            'total': total_questions,
            'percentage': round(percentage_score, 1)
        }
        
        return redirect('quizzes:quiz_results', quiz_id=quiz.id)
    
    # GET request - show quiz form
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

# 4. Show quiz results
def quiz_results(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    
    # Get results from session
    quiz_results = request.session.get('quiz_results', {})
    
    # Clear results from session after displaying
    if 'quiz_results' in request.session:
        del request.session['quiz_results']
    
    return render(request, 'quizzes/results.html', {
        'quiz': quiz,
        'results': quiz_results
    })

# 5. Analytics view for performance analysis
def quiz_analytics(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions_data = []
    
    for question in quiz.questions.all():
        choices_data = []
        total_votes = sum(choice.votes for choice in question.choices.all())
        
        for choice in question.choices.all():
            percentage = (choice.votes / total_votes * 100) if total_votes > 0 else 0
            choices_data.append({
                'text': choice.text,
                'votes': choice.votes,
                'percentage': round(percentage, 1),
                'is_correct': choice.is_correct
            })
        
        questions_data.append({
            'question': question,
            'choices': choices_data,
            'total_votes': total_votes
        })
    
    return render(request, 'quizzes/analytics.html', {
        'quiz': quiz,
        'questions_data': questions_data
    })
