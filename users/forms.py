from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, College
from django.contrib.auth import get_user_model

User = get_user_model()

class TeacherSignupForm(UserCreationForm):
    full_name = forms.CharField(max_length=150, label="Full Name", required=True)
    email = forms.EmailField(required=True)
    subjects = forms.CharField(max_length=200, required=True)
    experience = forms.IntegerField(required=False)
    profile_pic = forms.ImageField(required=False)
    college_key = forms.CharField(max_length=50, label="College Teacher Key", required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']  # Only include actual model fields

    def clean_college_key(self):
        key = self.cleaned_data.get('college_key')
        if not College.objects.filter(teacher_signup_key=key).exists():
            raise forms.ValidationError("Invalid College Teacher Key")
        return key

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "teacher"
        user.first_name = self.cleaned_data.get("full_name")
        user.email = self.cleaned_data.get("email")
        user.subjects = self.cleaned_data.get("subjects")
        user.experience = self.cleaned_data.get("experience", 0)
        
        college_key = self.cleaned_data.get("college_key")
        user.college = College.objects.get(teacher_signup_key=college_key)
        
        if commit:
            user.save()
        return user

class StudentSignupForm(UserCreationForm):
    full_name = forms.CharField(max_length=150, label="Full Name", required=True)
    email = forms.EmailField(required=True)
    student_class = forms.CharField(max_length=50, label="Class", required=True)
    roll_no = forms.CharField(max_length=50, required=True)
    academic_year = forms.CharField(max_length=50, required=True)
    college_key = forms.CharField(max_length=50, label="College Key", required=True)
    bio = forms.CharField(widget=forms.Textarea, required=False, label="About Yourself")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_college_key(self):
        key = self.cleaned_data.get('college_key')
        if not key:
            raise forms.ValidationError("College key is required.")
        
        try:
            college = College.objects.get(student_signup_key=key)
        except College.DoesNotExist:
            raise forms.ValidationError("Invalid college key. Please check with your institution.")
        return key

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "student"
        user.first_name = self.cleaned_data.get("full_name")
        user.email = self.cleaned_data.get("email")
        user.class_name = self.cleaned_data.get("student_class")
        user.roll_no = self.cleaned_data.get("roll_no")
        user.academic_year = self.cleaned_data.get("academic_year")
        user.bio = self.cleaned_data.get("bio", "")
        
        college_key = self.cleaned_data.get("college_key")
        user.college = College.objects.get(student_signup_key=college_key)
        
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput)

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'experience', 'bio', 'profile_pic', 'subjects']

class StudentEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "class_name", "roll_no", "academic_year", "bio"]