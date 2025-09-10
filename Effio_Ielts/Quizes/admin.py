from django.contrib import admin
from .models import Quiz, Question, Choice

# Register your models here.

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'due_date')
    list_filter = ('created_at', 'due_date')
    search_fields = ('title', 'description')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'created_at')
    list_filter = ('quiz', 'created_at')
    search_fields = ('text',)

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct', 'votes')
    list_filter = ('is_correct', 'question__quiz')
    search_fields = ('text',)
