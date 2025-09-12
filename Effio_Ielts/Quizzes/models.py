from django.db import models
from django.contrib.auth.models import User

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
        verbose_name_plural = "Quizzes"
    
    def __str__(self):
        return self.title

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

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    image = models.ImageField(upload_to='choice_images/', blank=True, null=True)  # New field
    is_correct = models.BooleanField(default=False)
    votes = models.IntegerField(default=0)  # Track how many students selected this choice
    
    def __str__(self):
        return f"{self.question.text[:30]} - {self.text}"

