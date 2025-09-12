from django.urls import path
from . import views

app_name = 'quizzes'  # Namespace for URL names

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),                                        # /quizzes/
    path('<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),                      # /quizzes/1/
    path('<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),                     # /quizzes/1/take/
    path('<int:quiz_id>/results/<int:attempt_id>/', views.quiz_results, name='quiz_results'),  # /quizzes/1/results/123/
    path('<int:quiz_id>/analytics/', views.quiz_analytics, name='quiz_analytics'),     # /quizzes/1/analytics/
    path('dashboard/', views.user_dashboard, name='user_dashboard'),                   # /quizzes/dashboard/
]