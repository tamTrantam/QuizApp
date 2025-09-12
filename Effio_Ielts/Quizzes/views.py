from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.db.models import Avg, Count, Q
from .models import Quiz, Question, Choice, QuizAttempt, QuizAnswer
import random
from datetime import timedelta, datetime

# Public view - anyone can see the list
def quiz_list(request):
    quizzes = Quiz.objects.all()  # Get all quizzes from database
    return render(request, 'quizzes/quiz_list.html', {'quizzes': quizzes})

# Public view - anyone can see details
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    
    # Get user's previous attempts if logged in
    user_attempts = []
    if request.user.is_authenticated:
        user_attempts = QuizAttempt.objects.filter(
            user=request.user, 
            quiz=quiz
        ).order_by('-completed_at')[:5]  # Last 5 attempts
    
    # Get quiz statistics
    stats = {
        'total_attempts': quiz.get_total_attempts(),
        'average_score': round(quiz.get_average_score(), 1),
        'total_questions': quiz.questions.count()
    }
    
    context = {
        'quiz': quiz,
        'user_attempts': user_attempts,
        'stats': stats
    }
    
    return render(request, 'quizzes/quiz_detail.html', context)

# Protected view - login required
@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    
    # Store start time in session if not already set
    if 'quiz_start_time' not in request.session:
        request.session['quiz_start_time'] = timezone.now().isoformat()
    
    if request.method == 'POST':
        # Calculate time taken
        start_time_str = request.session.get('quiz_start_time')
        if start_time_str:
            start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
            if timezone.is_naive(start_time):
                start_time = timezone.make_aware(start_time)
            time_taken = timezone.now() - start_time
        else:
            start_time = timezone.now()
            time_taken = timedelta(0)
        
        # Create quiz attempt
        attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=0,  # Will be updated below
            total_questions=quiz.questions.count(),
            percentage_score=0,  # Will be updated below
            time_taken=time_taken,
            started_at=start_time,
            ip_address=get_client_ip(request)
        )
        
        # Process each question and create detailed answers
        score = 0
        total_questions = quiz.questions.count()
        
        for question in quiz.questions.all():
            selected_choice_id = request.POST.get(f'question_{question.id}')
            selected_choice = None
            is_correct = False
            
            if selected_choice_id:
                try:
                    selected_choice = Choice.objects.get(id=selected_choice_id)
                    # Increment vote count for analytics
                    selected_choice.votes += 1
                    selected_choice.save()
                    
                    # Check if answer is correct
                    is_correct = selected_choice.is_correct
                    if is_correct:
                        score += 1
                        
                except Choice.DoesNotExist:
                    pass
            
            # Create detailed answer record
            QuizAnswer.objects.create(
                attempt=attempt,
                question=question,
                selected_choice=selected_choice,
                is_correct=is_correct
            )
        
        # Update attempt with final scores
        percentage_score = (score / total_questions * 100) if total_questions > 0 else 0
        attempt.score = score
        attempt.percentage_score = percentage_score
        attempt.save()
        
        # Clear start time from session
        if 'quiz_start_time' in request.session:
            del request.session['quiz_start_time']
        
        # Add success message
        messages.success(request, f'Quiz completed! You scored {score}/{total_questions} ({percentage_score:.1f}%)')
        
        return redirect('quizzes:quiz_results', quiz_id=quiz.id, attempt_id=attempt.id)
    
    # GET request - show quiz form
    questions = quiz.questions.all()
    
    # Randomize choices for each question
    for question in questions:
        choices = list(question.choices.all())
        random.shuffle(choices)  # This is where you randomize!
        question.shuffled_choices = choices
    
    context = {
        'quiz': quiz,
        'questions': questions,
        'total_questions': len(questions)
    }
    
    return render(request, 'quizzes/take_quiz.html', context)

# Protected view - login required  
@login_required
def quiz_results(request, quiz_id, attempt_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    attempt = get_object_or_404(QuizAttempt, pk=attempt_id, user=request.user, quiz=quiz)
    
    # Get detailed answers for review
    answers = QuizAnswer.objects.filter(attempt=attempt).select_related(
        'question', 'selected_choice'
    ).order_by('question__created_at')
    
    # Calculate detailed statistics
    stats = {
        'correct_answers': attempt.score,
        'total_questions': attempt.total_questions,
        'percentage': attempt.percentage_score,
        'grade': attempt.grade_letter,
        'performance_level': attempt.performance_label,
        'time_taken': attempt.time_taken,
        'rank': get_user_rank(attempt)
    }
    
    # Get user's attempt history for this quiz
    user_attempts = QuizAttempt.objects.filter(
        user=request.user,
        quiz=quiz
    ).order_by('-completed_at')
    
    # Improvement analysis
    improvement_data = None
    if user_attempts.count() > 1:
        previous_attempt = user_attempts[1]  # Second most recent
        improvement_data = {
            'previous_score': previous_attempt.percentage_score,
            'current_score': attempt.percentage_score,
            'improvement': attempt.percentage_score - previous_attempt.percentage_score
        }
    
    context = {
        'quiz': quiz,
        'attempt': attempt,
        'answers': answers,
        'stats': stats,
        'user_attempts': user_attempts,
        'improvement_data': improvement_data
    }
    
    return render(request, 'quizzes/results.html', context)

# Analytics view for performance analysis
@login_required
def quiz_analytics(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    
    # Overall quiz statistics
    total_attempts = QuizAttempt.objects.filter(quiz=quiz).count()
    avg_score = QuizAttempt.objects.filter(quiz=quiz).aggregate(
        avg_score=Avg('percentage_score')
    )['avg_score'] or 0
    
    # Question-level analytics
    questions_data = []
    for question in quiz.questions.all():
        # Get success rate for this question
        total_answers = QuizAnswer.objects.filter(question=question).count()
        correct_answers = QuizAnswer.objects.filter(question=question, is_correct=True).count()
        success_rate = (correct_answers / total_answers * 100) if total_answers > 0 else 0
        
        # Get choice distribution
        choices_data = []
        for choice in question.choices.all():
            choice_count = QuizAnswer.objects.filter(
                question=question, 
                selected_choice=choice
            ).count()
            percentage = (choice_count / total_answers * 100) if total_answers > 0 else 0
            
            choices_data.append({
                'text': choice.text,
                'count': choice_count,
                'percentage': round(percentage, 1),
                'is_correct': choice.is_correct
            })
        
        questions_data.append({
            'question': question,
            'success_rate': round(success_rate, 1),
            'total_answers': total_answers,
            'choices': choices_data
        })
    
    # Performance distribution
    performance_distribution = {
        'excellent': QuizAttempt.objects.filter(quiz=quiz, percentage_score__gte=90).count(),
        'good': QuizAttempt.objects.filter(quiz=quiz, percentage_score__gte=80, percentage_score__lt=90).count(),
        'average': QuizAttempt.objects.filter(quiz=quiz, percentage_score__gte=70, percentage_score__lt=80).count(),
        'below_average': QuizAttempt.objects.filter(quiz=quiz, percentage_score__gte=60, percentage_score__lt=70).count(),
        'poor': QuizAttempt.objects.filter(quiz=quiz, percentage_score__lt=60).count(),
    }
    
    context = {
        'quiz': quiz,
        'total_attempts': total_attempts,
        'avg_score': round(avg_score, 1),
        'questions_data': questions_data,
        'performance_distribution': performance_distribution
    }
    
    return render(request, 'quizzes/analytics.html', context)

# User dashboard showing quiz history
@login_required
def user_dashboard(request):
    # Get user's quiz attempts
    recent_attempts = QuizAttempt.objects.filter(
        user=request.user
    ).select_related('quiz').order_by('-completed_at')[:10]
    
    # Calculate user statistics
    total_quizzes_taken = QuizAttempt.objects.filter(user=request.user).values('quiz').distinct().count()
    total_attempts = QuizAttempt.objects.filter(user=request.user).count()
    avg_score = QuizAttempt.objects.filter(user=request.user).aggregate(
        avg_score=Avg('percentage_score')
    )['avg_score'] or 0
    
    # Get performance trend (last 10 attempts)
    performance_trend = list(recent_attempts.values_list('percentage_score', flat=True))
    
    # Best and worst performances
    best_attempt = QuizAttempt.objects.filter(user=request.user).order_by('-percentage_score').first()
    worst_attempt = QuizAttempt.objects.filter(user=request.user).order_by('percentage_score').first()
    
    context = {
        'recent_attempts': recent_attempts,
        'stats': {
            'total_quizzes_taken': total_quizzes_taken,
            'total_attempts': total_attempts,
            'avg_score': round(avg_score, 1),
            'performance_trend': performance_trend
        },
        'best_attempt': best_attempt,
        'worst_attempt': worst_attempt
    }
    
    return render(request, 'quizzes/user_dashboard.html', context)

# Helper functions
def get_client_ip(request):
    """Get the client's IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_user_rank(attempt):
    """Get user's rank compared to other users for this quiz"""
    better_attempts = QuizAttempt.objects.filter(
        quiz=attempt.quiz,
        percentage_score__gt=attempt.percentage_score
    ).count()
    return better_attempts + 1
