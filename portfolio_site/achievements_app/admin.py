from django.contrib import admin
from .models import Achievement


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date')
    list_filter = ('category',)
    search_fields = ('title',)
    ordering = ('-date',)
