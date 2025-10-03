from django.contrib.auth.models import AbstractUser
from django.db import models

class College(models.Model):
    name = models.CharField(max_length=100)
    teacher_signup_key = models.CharField(max_length=50)
    student_signup_key = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    bio = models.TextField(blank=True, null=True)  
    college = models.ForeignKey(College, on_delete=models.CASCADE, null=True, blank=True)

    # for Teacher
    subjects = models.CharField(max_length=200, blank=True, default='')
    experience = models.IntegerField(default=0)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # for Student
    class_name = models.CharField(max_length=50, blank=True, default='')
    roll_no = models.CharField(max_length=20, blank=True, default='')
    academic_year = models.CharField(max_length=20, blank=True, default='')

    def __str__(self):
        return f"{self.username} ({self.role})"

from django.utils import timezone

class LiveClass(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('live', 'Live'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    teacher = models.ForeignKey('CustomUser', on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    subject = models.CharField(max_length=100)
    scheduled_time = models.DateTimeField()
    duration = models.IntegerField(help_text="Duration in minutes", default=60)
    zoom_meeting_id = models.CharField(max_length=50, blank=True, null=True)
    zoom_join_url = models.URLField(blank=True, null=True)
    zoom_start_url = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-scheduled_time']
    
    def __str__(self):
        return f"{self.title} - {self.teacher.username}"
    
    def is_live_now(self):
        if self.status == 'live':
            return True
        start_time = self.scheduled_time
        end_time = start_time + timezone.timedelta(minutes=self.duration)
        return start_time <= timezone.now() <= end_time

class ClassEnrollment(models.Model):
    live_class = models.ForeignKey(LiveClass, on_delete=models.CASCADE)
    student = models.ForeignKey('CustomUser', on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    enrolled_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['live_class', 'student']
    
    def __str__(self):
        return f"{self.student.username} - {self.live_class.title}"




