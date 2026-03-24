from django.contrib import admin
from .models import Profile, Education


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'role', 'email_contact')
    search_fields = ('name', 'user__username')


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('course', 'institution_name', 'start_date', 'is_current', 'profile')
    list_filter = ('is_current',)
    search_fields = ('course', 'institution_name')
