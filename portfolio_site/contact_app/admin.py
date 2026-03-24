from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'timestamp', 'is_read')
    list_filter = ('is_read',)
    search_fields = ('name', 'email')
    list_editable = ('is_read',)
    readonly_fields = ('timestamp',)
