from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured', 'created_date')
    list_filter = ('featured',)
    search_fields = ('title', 'tech_stack')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('featured',)
