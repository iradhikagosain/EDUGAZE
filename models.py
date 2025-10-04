from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings

# Get the custom user model
User = get_user_model()

def user_directory_path(instance, filename): 
    name, ext = filename.split(".")
    name = instance.firstname + instance.lastname
    filename = name +'.'+ ext 
    return 'Faculty_Images/{}'.format(filename)

class Faculty(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200, null=True, blank=True)
    lastname = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(upload_to=user_directory_path, null=True, blank=True)

    def __str__(self):
        return str(self.firstname + " " + self.lastname)

def student_directory_path(instance, filename): 
    name, ext = filename.split(".")
    name = instance.registration_id
    filename = name +'.'+ ext 
    return 'Student_Images/{}/{}/{}/{}'.format(instance.branch, instance.year, instance.section, filename)

class Student(models.Model):
    BRANCH = (
        ('CSE','CSE'),
        ('IT','IT'),
        ('ECE','ECE'),
        ('CHEM','CHEM'),
        ('MECH','MECH'),
        ('EEE','EEE'),
    )
    YEAR = (
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
    )
    SECTION = (
        ('A','A'),
        ('B','B'),
        ('C','C'),
    )

    id = models.BigAutoField(primary_key=True)
    firstname = models.CharField(max_length=200, null=True, blank=True)
    lastname = models.CharField(max_length=200, null=True, blank=True)
    registration_id = models.CharField(max_length=200, null=True, unique=True)
    branch = models.CharField(max_length=100, null=True, choices=BRANCH)
    year = models.CharField(max_length=100, null=True, choices=YEAR)
    section = models.CharField(max_length=100, null=True, choices=SECTION)
    profile_pic = models.ImageField(upload_to=student_directory_path, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    college = models.ForeignKey('users.College', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['registration_id']
        indexes = [
            models.Index(fields=['registration_id']),
            models.Index(fields=['branch', 'year', 'section']),
        ]

    def __str__(self):
        return f"{self.registration_id} - {self.firstname} {self.lastname}"
    
    def get_full_name(self):
        return f"{self.firstname} {self.lastname}".strip()

class Attendence(models.Model):
    id = models.BigAutoField(primary_key=True)
    faculty = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='faculty_attendance')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True, related_name='student_attendance')
    Faculty_Name = models.CharField(max_length=200, null=True, blank=True)
    Student_ID = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(auto_now_add=True, null=True)
    time = models.TimeField(auto_now_add=True, null=True)
    branch = models.CharField(max_length=200, null=True)
    year = models.CharField(max_length=200, null=True)
    section = models.CharField(max_length=200, null=True)
    period = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=200, null=True, default='Absent')
    subject = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['-date', '-time']
        indexes = [
            models.Index(fields=['date', 'student']),
            models.Index(fields=['branch', 'year', 'section']),
        ]
        unique_together = ['student', 'date', 'period']  # Prevent duplicate entries

    def __str__(self):
        return f"{self.Student_ID} - {self.date} - {self.period} - {self.status}"
    
    def save(self, *args, **kwargs):
        # Auto-populate fields from related objects if available
        if self.student and not self.Student_ID:
            self.Student_ID = self.student.registration_id
        if self.student and not self.branch:
            self.branch = self.student.branch
        if self.student and not self.year:
            self.year = self.student.year
        if self.student and not self.section:
            self.section = self.student.section
        if self.faculty and not self.Faculty_Name:
            self.Faculty_Name = self.faculty.get_full_name()
        
        super().save(*args, **kwargs)

class AttendanceRecord(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True, related_name='face_attendance')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='teacher_attendance')
    timestamp = models.DateTimeField(default=timezone.now)
    confidence = models.FloatField(default=0.0)
    status = models.CharField(max_length=20, default='Present')
    image_path = models.CharField(max_length=255, blank=True, null=True)
    branch = models.CharField(max_length=100, blank=True, null=True)
    year = models.CharField(max_length=100, blank=True, null=True)
    section = models.CharField(max_length=100, blank=True, null=True)
    subject = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['name']),
            models.Index(fields=['teacher', 'timestamp']),
        ]
        verbose_name = 'Face Recognition Attendance'
        verbose_name_plural = 'Face Recognition Attendance Records'

    def __str__(self):
        return f"{self.name} - {self.timestamp.strftime('%Y-%m-%d %H:%M')} - {self.confidence:.1f}%"
    
    def save(self, *args, **kwargs):
        # Try to find matching student and populate additional fields
        if not self.student:
            try:
                # Try to find student by name or other criteria
                student = Student.objects.filter(
                    models.Q(firstname__icontains=self.name) | 
                    models.Q(lastname__icontains=self.name) |
                    models.Q(registration_id__icontains=self.name)
                ).first()
                if student:
                    self.student = student
                    self.branch = student.branch
                    self.year = student.year
                    self.section = student.section
            except:
                pass
        
        super().save(*args, **kwargs)

# Additional models for better organization

class Subject(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects')
    branch = models.CharField(max_length=100, blank=True, null=True)
    year = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code}) - {self.teacher.get_full_name()}"

class ClassSchedule(models.Model):
    PERIOD_CHOICES = (
        ('1', 'Period 1'),
        ('2', 'Period 2'),
        ('3', 'Period 3'),
        ('4', 'Period 4'),
        ('5', 'Period 5'),
        ('6', 'Period 6'),
    )
    
    DAY_CHOICES = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    )
    
    id = models.BigAutoField(primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    branch = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    class Meta:
        ordering = ['day', 'period']
        unique_together = ['branch', 'year', 'section', 'day', 'period']
    
    def __str__(self):
        return f"{self.subject.name} - {self.branch} {self.year} {self.section} - {self.day} {self.period}"

class FaceEncoding(models.Model):
    id = models.BigAutoField(primary_key=True)
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='face_encoding')
    encoding_data = models.TextField(help_text="JSON encoded face encoding data")
    image_path = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Face Encoding'
        verbose_name_plural = 'Face Encodings'
    
    def __str__(self):
        return f"Face encoding for {self.student.registration_id}"

# Signal to create face encoding when student is created or updated
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Student)
def create_student_face_encoding(sender, instance, created, **kwargs):
    """
    Signal to automatically handle face encoding when student is created/updated
    This would integrate with your face recognition system
    """
    if created and instance.profile_pic:
        # Here you would add logic to generate face encoding
        # from the profile_pic and save to FaceEncoding model
        pass