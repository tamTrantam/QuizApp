from django.contrib import admin
from .models import Quiz, Question, Choice

# Register your models here.

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'due_date', 'background_color')
    list_filter = ('created_at', 'due_date')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text_preview', 'quiz', 'question_type', 'created_at')
    list_filter = ('quiz', 'question_type', 'created_at')
    search_fields = ('text',)
    
    def text_preview(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
    text_preview.short_description = "Question Text"

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct', 'votes')
    list_filter = ('is_correct', 'question__quiz')
    search_fields = ('text',)
    readonly_fields = ('votes',)  # Make votes read-only since it's auto-updated
