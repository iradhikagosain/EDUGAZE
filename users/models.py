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
