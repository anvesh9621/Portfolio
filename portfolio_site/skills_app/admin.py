from django.contrib import admin
from .models import Skill, SkillCategory


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SkillInline]
    ordering = ('order', 'name')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'icon_class', 'order')
    list_filter = ('category',)
    search_fields = ('name',)
    ordering = ('category', 'order', 'name')
