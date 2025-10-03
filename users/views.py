from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser, College
from resources.models import Note,Lecture
from django.shortcuts import get_object_or_404
from .forms import StudentEditForm,StudentSignupForm, TeacherSignupForm
from django.contrib.auth import get_user_model

def home(request):
    return render(request, "users/home.html")


def signup(request):
    if request.method == "POST":
        role = request.POST.get("role")
        
        if role == "teacher":
            form = TeacherSignupForm(request.POST, request.FILES)
        else:
            form = StudentSignupForm(request.POST)
        
        print(f"Form is valid: {form.is_valid()}")
        
        if form.is_valid():
            user = form.save()
            messages.success(request, f"{role.capitalize()} account created successfully!")
            return redirect("signup")
        else:
            print(f"Form errors: {form.errors}")
            return render(request, "users/signup.html", {"form": form, "role": role})
    else:
        return render(request, "users/signup.html", {"form": None, "role": None})
    

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.role != role:
                print(f"Role mismatch: expected {role}, got {user.role}")  
                messages.error(request, "Selected role does not match your account.")
                return redirect("login")
            auth_login(request, user)
            if user.role == "teacher":
                return redirect("teacher_dashboard")
            else:
                return redirect("student_dashboard")
        else:
            print("Authentication failed")  
            try:
                user_exists = CustomUser.objects.get(username=username)
                print(f"User exists but wrong password: {user_exists.username}") 
                messages.error(request, "Invalid password.")
            except CustomUser.DoesNotExist:
                print("User does not exist") 
                messages.error(request, "Invalid username or password.")
            return redirect("login")

    return render(request, "users/login.html")



def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")



@login_required
def teacher_dashboard(request):
    if request.user.role != "teacher":
        return redirect("login")
    
    notes = Note.objects.filter(teacher=request.user)
    lectures = Lecture.objects.filter(teacher=request.user)

    context = {
        "teacher": request.user,
        "notes": notes,
        "lectures": lectures,
    }
    return render(request, "users/teacher_dashboard.html", context)


@login_required
def student_dashboard(request):
    if request.user.role != "student":
        return redirect("login")
    
    student = request.user  
    context = {
        "student": student
    }
    return render(request, "users/student_dashboard.html", context)



@login_required
def edit_student_profile(request):
    student = request.user
    if request.method == "POST":
        form = StudentEditForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect("student_dashboard")
    else:
        form = StudentEditForm(instance=student)
    return render(request, "users/student_edit_profile.html", {"form": form})

@login_required
def delete_student_account(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        return redirect("home")  
    return render(request, "users/student_delete_account.html")


@login_required
def my_uploads(request):
    if request.user.role != "teacher":
        return redirect("login")

    notes = Note.objects.filter(teacher=request.user)  
    lectures = Lecture.objects.filter(teacher=request.user)  

    context = {
        "notes": notes,
        "lectures": lectures,
    }
    return render(request, "users/my_uploads.html", context)



from .forms import TeacherProfileForm

@login_required
def edit_teacher_profile(request):
    if request.user.role != "teacher":
        return redirect("login")

    if request.method == "POST":
        form = TeacherProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("teacher_dashboard")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TeacherProfileForm(instance=request.user)

    context = {
        "form": form
    }
    return render(request, "users/edit_teacher_profile.html", context)

@login_required
def delete_teacher_account(request):
    if request.user.role != "teacher":
        return redirect("login")

    if request.method == "POST":
     
        notes = Note.objects.filter(teacher=request.user)
        for note in notes:
            note.file.delete()  
            note.delete()       
     
        lectures = Lecture.objects.filter(teacher=request.user)
        for lecture in lectures:
            lecture.video.delete()  
            lecture.delete()        

        
        user = request.user
        logout(request)           
        user.delete()

        messages.success(request, "Your account and all uploads have been deleted successfully.")
        return redirect("home")

    return render(request, "users/delete_teacher_account.html")

@login_required
def teacher_profiles(request):
    if request.user.role != 'student':
        return redirect('login')
    teachers = CustomUser.objects.filter(
        role='teacher', 
        college=request.user.college
    ).exclude(subjects='')
    
    context = {
        'teachers': teachers
    }
    return render(request, 'users/teacher_profiles.html', context)

@login_required
def teacher_profile_detail(request, teacher_id):
    if request.user.role != 'student':
        return redirect('login')
    
    teacher = get_object_or_404(CustomUser, id=teacher_id, role='teacher')
    
    notes = Note.objects.filter(teacher=teacher)
    lectures = Lecture.objects.filter(teacher=teacher)
    
    context = {
        'teacher': teacher,
        'notes': notes,
        'lectures': lectures
    }
    return render(request, 'users/teacher_profile_detail.html', context)

def handler404(request,exception):
    return render(request,"error/404.html",status=404)

