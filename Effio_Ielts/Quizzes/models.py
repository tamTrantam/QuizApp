from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='quiz_covers/', blank=True, null=True)  # New field
    background_color = models.CharField(max_length=7, default='#ffffff')  # Hex color
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def get_cover_image_url(self):
        """Return cover image URL with fallback for missing files."""
        if self.cover_image:
            try:
                # Check if file exists, return URL if it does
                self.cover_image.url
                return self.cover_image.url
            except:
                # If file doesn't exist, return default image
                return '/static/homepage/images/default-quiz-cover.svg'
        return '/static/homepage/images/default-quiz-cover.svg'
    
    def has_valid_cover_image(self):
        """Check if quiz has a valid, accessible cover image."""
        return self.cover_image and hasattr(self.cover_image, 'url')
        verbose_name_plural = "Quizzes"
    
    def __str__(self):
        return self.title
    
    def get_average_score(self):
        """Calculate average score across all attempts"""
        attempts = self.attempts.all()
        if not attempts:
            return 0
        return sum(attempt.percentage_score for attempt in attempts) / len(attempts)
    
    def get_total_attempts(self):
        """Get total number of attempts for this quiz"""
        return self.attempts.count()

class Question(models.Model):
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('reading_comprehension', 'Reading Comprehension'),
        ('listening', 'Listening'),
    ]
    
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    question_type = models.CharField(max_length=25, choices=QUESTION_TYPES, default='multiple_choice')
    image = models.ImageField(upload_to='question_images/', blank=True, null=True)  # New field
    audio_file = models.FileField(upload_to='question_audio/', blank=True, null=True)  # New field
    reading_passage = models.TextField(blank=True, null=True)  # For reading questions
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.quiz.title} - {self.text[:50]}"
    
    def get_correct_answer(self):
        """Get the correct choice for this question"""
        return self.choices.filter(is_correct=True).first()
    
    def get_success_rate(self):
        """Calculate percentage of users who answered correctly"""
        total_answers = QuizAnswer.objects.filter(question=self).count()
        if total_answers == 0:
            return 0
        correct_answers = QuizAnswer.objects.filter(question=self, is_correct=True).count()
        return (correct_answers / total_answers) * 100

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    image = models.ImageField(upload_to='choice_images/', blank=True, null=True)  # New field
    is_correct = models.BooleanField(default=False)
    votes = models.IntegerField(default=0)  # Track how many students selected this choice
    
    def __str__(self):
        return f"{self.question.text[:30]} - {self.text}"
    
    def get_selection_percentage(self):
        """Get percentage of users who selected this choice"""
        total_votes = sum(choice.votes for choice in self.question.choices.all())
        if total_votes == 0:
            return 0
        return (self.votes / total_votes) * 100

class QuizAttempt(models.Model):
    """Track detailed quiz attempts and results"""
    PERFORMANCE_LEVELS = [
        ('excellent', 'Excellent (90-100%)'),
        ('good', 'Good (80-89%)'),
        ('average', 'Average (70-79%)'),
        ('below_average', 'Below Average (60-69%)'),
        ('poor', 'Poor (0-59%)'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.IntegerField()  # Number of correct answers
    total_questions = models.IntegerField()
    percentage_score = models.DecimalField(max_digits=5, decimal_places=2)
    time_taken = models.DurationField(null=True, blank=True)  # Time to complete quiz
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-completed_at']
        unique_together = ['user', 'quiz', 'completed_at']  # Allow multiple attempts
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.percentage_score}%"
    
    @property
    def performance_level(self):
        """Determine performance level based on percentage score"""
        if self.percentage_score >= 90:
            return 'excellent'
        elif self.percentage_score >= 80:
            return 'good'
        elif self.percentage_score >= 70:
            return 'average'
        elif self.percentage_score >= 60:
            return 'below_average'
        else:
            return 'poor'
    
    @property
    def performance_label(self):
        """Get human-readable performance label"""
        levels = dict(self.PERFORMANCE_LEVELS)
        return levels.get(self.performance_level, 'Unknown')
    
    @property
    def grade_letter(self):
        """Convert percentage to letter grade"""
        if self.percentage_score >= 90:
            return 'A'
        elif self.percentage_score >= 80:
            return 'B'
        elif self.percentage_score >= 70:
            return 'C'
        elif self.percentage_score >= 60:
            return 'D'
        else:
            return 'F'

class QuizAnswer(models.Model):
    """Track individual answers for detailed analytics"""
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, blank=True)
    is_correct = models.BooleanField()
    time_taken = models.DurationField(null=True, blank=True)  # Time to answer this question
    
    class Meta:
        unique_together = ['attempt', 'question']
    
    def __str__(self):
        return f"{self.attempt.user.username} - {self.question.text[:30]} - {'✓' if self.is_correct else '✗'}"

