from django.contrib import admin
from .models import Quiz, Question, QuizAttempt

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'difficulty', 'number_of_questions', 'created_at']
    list_filter = ['difficulty', 'subject', 'created_at']
    search_fields = ['title', 'subject']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'quiz', 'correct_answer']
    list_filter = ['quiz']
    search_fields = ['question_text']

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['student', 'quiz', 'score', 'total_questions', 'attempted_at']
    list_filter = ['quiz', 'attempted_at']
    search_fields = ['student__username', 'quiz__title']
    
    def percentage(self, obj):
        return f"{obj.percentage()}%"
    percentage.short_description = 'Percentage'