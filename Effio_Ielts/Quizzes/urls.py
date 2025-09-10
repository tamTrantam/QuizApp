from django.urls import path
from . import views

app_name = 'quizzes'  # Namespace for URL names

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),                    # /quizzes/
    path('<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),  # /quizzes/1/
    path('<int:quiz_id>/take/', views.take_quiz, name='take_quiz'), # /quizzes/1/take/
    path('<int:quiz_id>/results/', views.quiz_results, name='results'), # /quizzes/1/results/
]