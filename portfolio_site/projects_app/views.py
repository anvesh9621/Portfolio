from django.shortcuts import render, get_object_or_404
from .models import Project


def project_list_view(request):
    projects = Project.objects.all()
    context = {'projects': projects}
    return render(request, 'projects.html', context)

def project_detail_view(request, slug):
    project = get_object_or_404(Project, slug=slug)
    context = {'project': project}
    return render(request, 'project_detail.html', context)
