from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("teacher/dashboard/", views.teacher_dashboard, name="teacher_dashboard"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("student/edit-profile/", views.edit_student_profile, name="edit_student_profile"),
    path("student/delete-account/", views.delete_student_account, name="delete_student_account"),
    path("my_uploads/", views.my_uploads, name="my_uploads"),
    path("teacher-profiles/", views.teacher_profiles, name="teacher_profiles"),
    path("teacher-profile/<int:teacher_id>/", views.teacher_profile_detail, name="teacher_profile_detail"),
    path("edit_teacher_profile/", views.edit_teacher_profile, name="edit_teacher_profile"),
    path("delete_teacher_account/", views.delete_teacher_account, name="delete_teacher_account"),
    
]

handler404 = "edugaze.views.handler404"

