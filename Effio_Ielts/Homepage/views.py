from django.shortcuts import render
from Quizzes.models import Quiz

# Create your views here.

def home(request):
    # Get featured quizzes for homepage (latest 3)
    featured_quizzes = Quiz.objects.all()[:3]
    
    context = {
        'featured_quizzes': featured_quizzes,
    }
    return render(request, 'homepage/home.html', context)

def about(request):
    return render(request, 'homepage/about.html')

def contact(request):
    return render(request, 'homepage/contact.html')