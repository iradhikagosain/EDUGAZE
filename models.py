from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Quiz(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    number_of_questions = models.IntegerField()
    time_limit = models.IntegerField(default=30, help_text="Time limit in minutes") 
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.subject} ({self.difficulty})"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=1, choices=[
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ])
    
    def __str__(self):
        return self.question_text[:50]

class QuizAttempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True)  # Make optional
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    attempted_at = models.DateTimeField(auto_now_add=True)
    time_taken = models.IntegerField(default=0, help_text="Time taken in seconds")
    subject = models.CharField(max_length=200, blank=True)  # Add subject field
    difficulty = models.CharField(max_length=10, blank=True)  # Add difficulty field
    
    def __str__(self):
        if self.quiz:
            return f"{self.student.username} - {self.quiz.title} - Score: {self.score}/{self.total_questions}"
        else:
            return f"{self.student.username} - AI Quiz - Score: {self.score}/{self.total_questions}"
    
    def percentage(self):
        if self.total_questions > 0:
            return (self.score / self.total_questions) * 100
        return 0


    