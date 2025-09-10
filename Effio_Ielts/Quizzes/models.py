from django.db import models


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # Automatically set the field to now when the object is first created.
    due_date = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True) # Automatically set the field to now every time the object is saved.
    class Meta:
        ordering = ['-due_date']  # Show newest quizzes first
        verbose_name_plural = "Quizzes"  # Fix "Quizs" in admin
    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['text']  # Show questions in alphabetical order
    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    votes = models.IntegerField(default=0)

    class Meta:
        ordering = ['-votes', 'text']  # Correct choices first, then alphabetical
    def __str__(self):
        return self.text
    
