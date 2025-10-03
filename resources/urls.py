from django.urls import path
from . import views

urlpatterns = [
    path("upload-note/", views.upload_note, name="upload_note"),
    path("delete-note/<int:note_id>/", views.delete_note, name="delete_note"),
    path("upload-lecture/", views.upload_lecture, name="upload_lecture"),
    path("delete-lecture/<int:lecture_id>/", views.delete_lecture, name="delete_lecture"),
]
