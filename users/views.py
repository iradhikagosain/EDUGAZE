from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser, College
from resources.models import Note,Lecture
from django.shortcuts import get_object_or_404
from .forms import StudentEditForm,StudentSignupForm, TeacherSignupForm
from django.contrib.auth import get_user_model
from django.utils import timezone
from .zoom_api import ZoomAPI
from .models import LiveClass, ClassEnrollment, CustomUser
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404




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


#LIVE CLASSES


@login_required
def teacher_create_live_class(request):
    if request.user.role != 'teacher':
        messages.error(request, 'Only teachers can create live classes.')
        return redirect('home')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        subject = request.POST.get('subject')
        scheduled_time = request.POST.get('scheduled_time')
        duration = request.POST.get('duration', 60)
        
        zoom_api = ZoomAPI()
        meeting_data = zoom_api.create_meeting(
            topic=title,
            start_time=timezone.datetime.fromisoformat(scheduled_time),
            duration=int(duration)
        )
        
        if meeting_data:
            live_class = LiveClass.objects.create(
                teacher=request.user,
                title=title,
                description=description,
                subject=subject,
                scheduled_time=scheduled_time,
                duration=duration,
                zoom_meeting_id=meeting_data['meeting_id'],
                zoom_join_url=meeting_data['join_url'],
                zoom_start_url=meeting_data['start_url'],
                status='scheduled'
            )
            messages.success(request, 'Live class created successfully!')
            return redirect('teacher_live_classes')
        else:
            messages.error(request, 'Failed to create Zoom meeting.')
    
    return render(request, 'users/teacher_create_live_class.html')

@login_required
def teacher_live_classes(request):
    if request.user.role != 'teacher':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    classes = LiveClass.objects.filter(teacher=request.user)
    return render(request, 'users/teacher_live_classes.html', {'classes': classes})

@login_required
def start_live_class(request, class_id):
    if request.user.role != 'teacher':
        messages.error(request, 'Only teachers can start live classes.')
        return redirect('home')
    
    live_class = get_object_or_404(LiveClass, id=class_id, teacher=request.user)
    
    live_class.status = 'live'
    live_class.save()
    

    if live_class.zoom_start_url:
        return redirect(live_class.zoom_start_url)
    else:
        messages.error(request, 'No Zoom meeting found for this class.')
        return redirect('teacher_live_classes')

@login_required
def end_live_class(request, class_id):
    if request.user.role != 'teacher':
        messages.error(request, 'Only teachers can end live classes.')
        return redirect('home')
    
    live_class = get_object_or_404(LiveClass, id=class_id, teacher=request.user)
    live_class.status = 'completed'
    live_class.save()
    messages.success(request, 'Live class ended successfully!')
    return redirect('teacher_live_classes')


@login_required
def student_live_classes(request):
    if request.user.role != 'student':
        messages.error(request, 'Access denied.')
        return redirect('home')
    

    classes = LiveClass.objects.filter(
        status__in=['scheduled', 'live']
    ).order_by('scheduled_time')
    
    for class_obj in classes:
        class_obj.is_enrolled = ClassEnrollment.objects.filter(
            live_class=class_obj, 
            student=request.user
        ).exists()
        class_obj.can_join = class_obj.is_live_now()
    
    return render(request, 'users/student_live_classes.html', {'classes': classes})

@login_required
def enroll_live_class(request, class_id):
    if request.user.role != 'student':
        messages.error(request, 'Only students can enroll in classes.')
        return redirect('home')
    
    live_class = get_object_or_404(LiveClass, id=class_id)
    
  
    if not ClassEnrollment.objects.filter(live_class=live_class, student=request.user).exists():
        ClassEnrollment.objects.create(live_class=live_class, student=request.user)
        messages.success(request, f'Successfully enrolled in {live_class.title}')
    else:
        messages.info(request, 'You are already enrolled in this class')
    
    return redirect('student_live_classes')

@login_required
def join_live_class(request, class_id):
    if request.user.role != 'student':
        messages.error(request, 'Only students can join classes.')
        return redirect('home')
    
    live_class = get_object_or_404(LiveClass, id=class_id)
    
    
    if not ClassEnrollment.objects.filter(live_class=live_class, student=request.user).exists():
        messages.error(request, 'You need to enroll in this class first.')
        return redirect('student_live_classes')
    
  
    if live_class.is_live_now():
        if live_class.zoom_join_url:
            return redirect(live_class.zoom_join_url)
        else:
            messages.error(request, 'No meeting link available.')
    else:
        messages.warning(request, 'Class is not live yet. Please wait for the scheduled time.')
    
    return redirect('student_live_classes')



def handler404(request,exception):
    return render(request,"error/404.html",status=404)

@login_required
def test_zoom_connection(request):
    """Test Zoom API connection"""
    if request.user.role != 'teacher':
        messages.error(request, 'Only teachers can access this page.')
        return redirect('home')
    
    from .zoom_api import ZoomAPI
    
    zoom_api = ZoomAPI()
    access_token = zoom_api.get_access_token()
    
    if access_token:
       
        test_meeting = zoom_api.create_meeting(
            topic="Test Meeting - EduGaze",
            start_time=timezone.now() + timezone.timedelta(hours=1),
            duration=30
        )
        
        if test_meeting:
            messages.success(request, f'Zoom connection successful! Meeting created: {test_meeting["meeting_id"]}')
        else:
            messages.error(request, 'Zoom connection failed - could not create meeting')
    else:
        messages.error(request, 'Zoom connection failed - could not get access token')
    
    return redirect('teacher_live_classes')