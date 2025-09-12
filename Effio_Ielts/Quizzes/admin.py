from django.contrib import admin
from .models import Quiz, Question, Choice, QuizAttempt, QuizAnswer

# Register your models here.

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'due_date', 'background_color', 'total_attempts', 'avg_score')
    list_filter = ('created_at', 'due_date')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    def total_attempts(self, obj):
        return obj.get_total_attempts()
    total_attempts.short_description = "Total Attempts"
    
    def avg_score(self, obj):
        return f"{obj.get_average_score():.1f}%"
    avg_score.short_description = "Average Score"

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text_preview', 'quiz', 'question_type', 'created_at', 'success_rate')
    list_filter = ('quiz', 'question_type', 'created_at')
    search_fields = ('text',)
    
    def text_preview(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
    text_preview.short_description = "Question Text"
    
    def success_rate(self, obj):
        return f"{obj.get_success_rate():.1f}%"
    success_rate.short_description = "Success Rate"

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct', 'votes', 'selection_percentage')
    list_filter = ('is_correct', 'question__quiz')
    search_fields = ('text',)
    readonly_fields = ('votes',)  # Make votes read-only since it's auto-updated
    
    def selection_percentage(self, obj):
        return f"{obj.get_selection_percentage():.1f}%"
    selection_percentage.short_description = "Selection %"

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'percentage_score', 'grade_letter', 'performance_level_display', 'completed_at', 'time_taken')
    list_filter = ('quiz', 'completed_at')
    search_fields = ('user__username', 'quiz__title')
    readonly_fields = ('completed_at', 'performance_level_display', 'grade_letter')
    date_hierarchy = 'completed_at'
    
    def performance_level_display(self, obj):
        return obj.performance_level
    performance_level_display.short_description = "Performance"

class QuizAnswerInline(admin.TabularInline):
    model = QuizAnswer
    extra = 0
    readonly_fields = ('question', 'selected_choice', 'is_correct')

@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt_user', 'question_text', 'selected_choice', 'is_correct', 'attempt_date')
    list_filter = ('is_correct', 'attempt__quiz', 'attempt__completed_at')
    search_fields = ('attempt__user__username', 'question__text')
    readonly_fields = ('attempt', 'question', 'selected_choice', 'is_correct')
    
    def attempt_user(self, obj):
        return obj.attempt.user.username
    attempt_user.short_description = "User"
    
    def question_text(self, obj):
        return obj.question.text[:50] + "..." if len(obj.question.text) > 50 else obj.question.text
    question_text.short_description = "Question"
    
    def attempt_date(self, obj):
        return obj.attempt.completed_at
    attempt_date.short_description = "Date"

# Add QuizAnswer inline to QuizAttempt admin
QuizAttemptAdmin.inlines = [QuizAnswerInline]
