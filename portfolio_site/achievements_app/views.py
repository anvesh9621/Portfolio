from django.shortcuts import render
from .models import Achievement


def achievements_view(request):
    achievements = Achievement.objects.all()
    return render(request, 'achievements.html', {'achievements': achievements})
