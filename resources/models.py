from django.db import models
from users.models import CustomUser

class Note(models.Model):
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role':'teacher'})
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='notes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True) 

    def __str__(self):
        return self.title

class Lecture(models.Model):
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role':'teacher'})
    title = models.CharField(max_length=200)
    video = models.FileField(upload_to='lectures/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True) 

    def __str__(self):
        return self.title
