from django.db import models
from django.utils.text import slugify


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    summary = models.CharField(max_length=300, help_text="Short one-line summary")
    description = models.TextField()
    tech_stack = models.CharField(max_length=400, help_text="Comma-separated: Python, Django, ...")
    github_link = models.URLField()
    live_demo_link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    featured = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-featured', '-created_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_tech_list(self):
        """Returns tech stack as a list."""
        return [t.strip() for t in self.tech_stack.split(',') if t.strip()]

    def get_card_bullets(self):
        """Returns up to 3 bullet points extracted from the description."""
        lines = [line.strip().lstrip('-').lstrip('•').lstrip('*').strip() for line in self.description.split('\n') if line.strip()]
        return lines[:3]

    def __str__(self):
        return self.title
