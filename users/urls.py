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
    path('teacher/live-classes/', views.teacher_live_classes, name='teacher_live_classes'),
    path('teacher/create-live-class/', views.teacher_create_live_class, name='teacher_create_live_class'),
    path('teacher/start-live-class/<int:class_id>/', views.start_live_class, name='start_live_class'),
    path('teacher/end-live-class/<int:class_id>/', views.end_live_class, name='end_live_class'),
    path('student/live-classes/', views.student_live_classes, name='student_live_classes'),
    path('student/enroll-live-class/<int:class_id>/', views.enroll_live_class, name='enroll_live_class'),
    path('student/join-live-class/<int:class_id>/', views.join_live_class, name='join_live_class'),
    path('test-zoom/', views.test_zoom_connection, name='test_zoom_connection'),
    
]

handler404 = "edugaze.views.handler404"

