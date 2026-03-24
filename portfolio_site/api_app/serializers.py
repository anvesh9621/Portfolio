from rest_framework import serializers
from projects_app.models import Project
from contact_app.models import ContactMessage


class ProjectSerializer(serializers.ModelSerializer):
    tech_list = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'summary', 'description',
            'tech_stack', 'tech_list', 'github_link', 'live_demo_link',
            'image', 'featured', 'created_date',
        ]
        read_only_fields = ['slug', 'created_date']

    def get_tech_list(self, obj):
        return obj.get_tech_list()

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters.")
        return value


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'message', 'timestamp']
        read_only_fields = ['timestamp']

    def validate_message(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Message must be at least 10 characters.")
        return value

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty.")
        return value
