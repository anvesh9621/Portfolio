from django.db import models


class Achievement(models.Model):
    CATEGORY_CHOICES = [
        ('Certification', 'Certification'),
        ('Hackathon', 'Hackathon'),
        ('Award', 'Award'),
        ('Recognition', 'Recognition'),
        ('Education', 'Education'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='achievements/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    date = models.DateField()
    url_link = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title
