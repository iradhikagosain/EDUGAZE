from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_home, name='quiz_home'),
    path('take/', views.take_quiz, name='take_quiz'),
    path('append-questions/', views.append_questions, name='append_questions'),
    path('submit/', views.submit_quiz, name='submit_quiz'),
    path('report/', views.generate_report, name='generate_report'),
    path('history/', views.quiz_history, name='quiz_history'),
    path('debug/', views.debug_quiz, name='debug_quiz'),
]

