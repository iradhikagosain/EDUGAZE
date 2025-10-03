from django.contrib import admin
from .models import CustomUser, College
from django.contrib.auth.admin import UserAdmin


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher_signup_key', 'student_signup_key')
    search_fields = ('name',)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'college', 'is_staff', 'is_active')
    list_filter = ('role', 'college', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'role', 'college')}),
        ('Personal Info', {'fields': ('bio', 'profile_pic', 'subjects', 'experience', 'class_name', 'roll_no', 'academic_year')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'college', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
