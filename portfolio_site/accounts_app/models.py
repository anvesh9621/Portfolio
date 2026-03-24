from django.db import models
from django.contrib.auth.models import User
import re


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    bio = models.TextField(help_text="Short bio for the hero section")
    about_bio = models.TextField(
        blank=True,
        help_text="Extended bio for the About page"
    )
    profile_image = models.ImageField(
        upload_to='profile_images/', blank=True, null=True
    )
    skills = models.TextField(
        help_text="Comma-separated skills (legacy field)",
        blank=True
    )
    github_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    email_contact = models.EmailField(blank=True, null=True)
    role = models.CharField(
        max_length=200,
        default="Full Stack Developer",
        help_text="Comma-separated roles for animated hero section (e.g. Backend Dev, Data Scientist)"
    )
    resume = models.URLField(
        blank=True, null=True,
        help_text="Paste your Google Drive share link (e.g. https://drive.google.com/file/d/.../view). Visitors will be able to view and download the PDF."
    )

    def __str__(self):
        return self.name

    @property
    def resume_download_url(self):
        """
        Convert a Google Drive share/view URL to a direct download URL.
        e.g. https://drive.google.com/file/d/FILE_ID/view?usp=sharing
          -> https://drive.google.com/uc?export=download&id=FILE_ID
        This ensures the browser downloads a properly named PDF file.
        Falls back to the raw URL for non-Drive links.
        """
        if not self.resume:
            return None
        match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', self.resume)
        if match:
            file_id = match.group(1)
            return f'https://drive.google.com/uc?export=download&id={file_id}'
        return self.resume


class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='educations')
    course = models.CharField(max_length=200)
    institution_name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    location = models.CharField(max_length=200)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.course} at {self.institution_name}"
