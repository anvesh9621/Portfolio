from django import forms
from projects_app.models import Project
from skills_app.models import Skill, SkillCategory
from achievements_app.models import Achievement
from .models import Profile, Education


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'role', 'bio', 'about_bio', 'profile_image',
                  'github_url', 'linkedin_url', 'email_contact', 'resume']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'about_bio': forms.Textarea(attrs={'rows': 6}),
            'resume': forms.URLInput(attrs={
                'placeholder': 'https://drive.google.com/file/d/YOUR_FILE_ID/view?usp=sharing'
            }),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'summary', 'description', 'tech_stack',
                  'github_link', 'live_demo_link', 'image', 'featured']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'tech_stack': forms.TextInput(attrs={
                'placeholder': 'Python, Django, PostgreSQL, ...'
            }),
        }


class SkillCategoryForm(forms.ModelForm):
    class Meta:
        model = SkillCategory
        fields = ['name', 'order']


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'icon_class', 'order']


class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ['title', 'image', 'category', 'date', 'url_link']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['course', 'institution_name', 'start_date', 'end_date', 'is_current', 'location']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
