from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Note, Lecture

@login_required
def upload_note(request):
    if request.method == "POST" and request.user.role == "teacher":
        title = request.POST.get("title")
        file = request.FILES.get("file")
        Note.objects.create(teacher=request.user, title=title, file=file)
        messages.success(request, "Note uploaded successfully!")
    return redirect("my_uploads")

@login_required
def delete_note(request, note_id):
    try:
        note = Note.objects.get(id=note_id, teacher=request.user)
        note.file.delete()
        note.delete()
        messages.success(request, "Note deleted successfully!")
    except Note.DoesNotExist:
        messages.error(request, "Note not found.")
    return redirect("my_uploads")

@login_required
def upload_lecture(request):
    if request.method == "POST" and request.user.role == "teacher":
        title = request.POST.get("title")
        video = request.FILES.get("video")
        Lecture.objects.create(teacher=request.user, title=title, video=video)
        messages.success(request, "Lecture uploaded successfully!")
    return redirect("my_uploads")

@login_required
def delete_lecture(request, lecture_id):
    try:
        lecture = Lecture.objects.get(id=lecture_id, teacher=request.user)
        lecture.video.delete()
        lecture.delete()
        messages.success(request, "Lecture deleted successfully!")
    except Lecture.DoesNotExist:
        messages.error(request, "Lecture not found.")
    return redirect("my_uploads")





