from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from projects_app.models import Project
from skills_app.models import Skill, SkillCategory
from achievements_app.models import Achievement
from contact_app.models import ContactMessage
from .models import Profile, Education
from .forms import ProfileForm, ProjectForm, SkillForm, AchievementForm, SkillCategoryForm, EducationForm


# ─── Public Views ────────────────────────────────────────────────────────────

def home_view(request):
    profile = Profile.objects.first()
    featured_projects = Project.objects.order_by('-created_date')[:3]
    categories = SkillCategory.objects.prefetch_related('skills').all()
    achievements = Achievement.objects.all()[:6]
    context = {
        'profile': profile,
        'featured_projects': featured_projects,
        'categories': categories,
        'achievements': achievements,
    }
    return render(request, 'home.html', context)


def about_view(request):
    profile = Profile.objects.first()
    categories = SkillCategory.objects.prefetch_related('skills').all()
    achievements = Achievement.objects.all()
    educations = profile.educations.all() if profile else []
    context = {
        'profile': profile,
        'categories': categories,
        'achievements': achievements,
        'educations': educations,
    }
    return render(request, 'about.html', context)


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('signup')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Account created! Please log in.')
        return redirect('login')

    return render(request, 'auth/signup.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials.')
            return redirect('login')
    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


# ─── Dashboard (superuser only) ───────────────────────────────────────────────

def superuser_check(user):
    return user.is_superuser


@login_required
@user_passes_test(superuser_check)
def dashboard_view(request):
    context = {
        'profile': Profile.objects.first(),
        'project_count': Project.objects.count(),
        'skill_count': Skill.objects.count(),
        'achievement_count': Achievement.objects.count(),
        'education_count': Profile.objects.first().educations.count() if Profile.objects.first() else 0,
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        'total_messages': ContactMessage.objects.count(),
        'featured_count': Project.objects.filter(featured=True).count(),
        'recent_messages': ContactMessage.objects.filter(is_read=False)[:5],
    }
    return render(request, 'dashboard/dashboard_home.html', context)


# ── Profile ──

@login_required
@user_passes_test(superuser_check)
def profile_edit_view(request):
    profile = Profile.objects.first()
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            prof = form.save(commit=False)
            if profile is None:
                prof.user = request.user
            prof.save()
            messages.success(request, 'Profile updated.')
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'dashboard/profile_form.html', {'form': form})


# ── Projects ──

@login_required
@user_passes_test(superuser_check)
def dashboard_projects_view(request):
    projects = Project.objects.all()
    return render(request, 'dashboard/project_list.html', {'projects': projects})


@login_required
@user_passes_test(superuser_check)
def add_project_view(request):
    form = ProjectForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Project added.')
        return redirect('dashboard_projects')
    return render(request, 'dashboard/project_form.html', {'form': form, 'action': 'Add'})


@login_required
@user_passes_test(superuser_check)
def edit_project_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectForm(request.POST or None, request.FILES or None, instance=project)
    if form.is_valid():
        form.save()
        messages.success(request, 'Project updated.')
        return redirect('dashboard_projects')
    return render(request, 'dashboard/project_form.html', {'form': form, 'action': 'Edit', 'obj': project})


@login_required
@user_passes_test(superuser_check)
def delete_project_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted.')
        return redirect('dashboard_projects')
    return render(request, 'dashboard/confirm_delete.html', {'obj': project, 'type': 'Project'})


@login_required
@user_passes_test(superuser_check)
def toggle_featured_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.featured = not project.featured
    project.save()
    return redirect('dashboard_projects')


# ── Skills & Categories ──

@login_required
@user_passes_test(superuser_check)
def dashboard_skills_view(request):
    categories = SkillCategory.objects.prefetch_related('skills').all()
    return render(request, 'dashboard/skill_list.html', {'categories': categories})


@login_required
@user_passes_test(superuser_check)
def add_skill_category_view(request):
    form = SkillCategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Skill Category added.')
        return redirect('dashboard_skills')
    return render(request, 'dashboard/skill_category_form.html', {'form': form, 'action': 'Add'})


@login_required
@user_passes_test(superuser_check)
def edit_skill_category_view(request, pk):
    category = get_object_or_404(SkillCategory, pk=pk)
    form = SkillCategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        messages.success(request, 'Skill Category updated.')
        return redirect('dashboard_skills')
    return render(request, 'dashboard/skill_category_form.html', {'form': form, 'action': 'Edit', 'obj': category})


@login_required
@user_passes_test(superuser_check)
def delete_skill_category_view(request, pk):
    category = get_object_or_404(SkillCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Skill Category deleted.')
        return redirect('dashboard_skills')
    return render(request, 'dashboard/confirm_delete.html', {'obj': category, 'type': 'Skill Category'})


@login_required
@user_passes_test(superuser_check)
def add_skill_view(request, category_id):
    category = get_object_or_404(SkillCategory, pk=category_id)
    form = SkillForm(request.POST or None)
    if form.is_valid():
        skill = form.save(commit=False)
        skill.category = category
        skill.save()
        messages.success(request, f'Skill added to {category.name}.')
        return redirect('dashboard_skills')
    return render(request, 'dashboard/skill_form.html', {'form': form, 'action': 'Add', 'category': category})


@login_required
@user_passes_test(superuser_check)
def edit_skill_view(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    form = SkillForm(request.POST or None, instance=skill)
    if form.is_valid():
        form.save()
        messages.success(request, 'Skill updated.')
        return redirect('dashboard_skills')
    return render(request, 'dashboard/skill_form.html', {'form': form, 'action': 'Edit', 'obj': skill, 'category': skill.category})


@login_required
@user_passes_test(superuser_check)
def delete_skill_view(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill deleted.')
        return redirect('dashboard_skills')
    return render(request, 'dashboard/confirm_delete.html', {'obj': skill, 'type': 'Skill'})


# ── Achievements ──

@login_required
@user_passes_test(superuser_check)
def dashboard_achievements_view(request):
    achievements = Achievement.objects.all()
    return render(request, 'dashboard/achievement_list.html', {'achievements': achievements})


@login_required
@user_passes_test(superuser_check)
def add_achievement_view(request):
    form = AchievementForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Achievement added.')
        return redirect('dashboard_achievements')
    return render(request, 'dashboard/achievement_form.html', {'form': form, 'action': 'Add'})


@login_required
@user_passes_test(superuser_check)
def edit_achievement_view(request, pk):
    achievement = get_object_or_404(Achievement, pk=pk)
    form = AchievementForm(request.POST or None, request.FILES or None, instance=achievement)
    if form.is_valid():
        form.save()
        messages.success(request, 'Achievement updated.')
        return redirect('dashboard_achievements')
    return render(request, 'dashboard/achievement_form.html', {
        'form': form, 'action': 'Edit', 'obj': achievement
    })


@login_required
@user_passes_test(superuser_check)
def delete_achievement_view(request, pk):
    achievement = get_object_or_404(Achievement, pk=pk)
    if request.method == 'POST':
        achievement.delete()
        messages.success(request, 'Achievement deleted.')
        return redirect('dashboard_achievements')
    return render(request, 'dashboard/confirm_delete.html', {'obj': achievement, 'type': 'Achievement'})


# ── Education ──

@login_required
@user_passes_test(superuser_check)
def dashboard_educations_view(request):
    profile = Profile.objects.first()
    educations = profile.educations.all() if profile else []
    return render(request, 'dashboard/education_list.html', {'educations': educations})


@login_required
@user_passes_test(superuser_check)
def add_education_view(request):
    profile = Profile.objects.first()
    form = EducationForm(request.POST or None)
    if form.is_valid():
        education = form.save(commit=False)
        education.profile = profile
        education.save()
        messages.success(request, 'Education added.')
        return redirect('dashboard_educations')
    return render(request, 'dashboard/education_form.html', {'form': form, 'action': 'Add'})


@login_required
@user_passes_test(superuser_check)
def edit_education_view(request, pk):
    education = get_object_or_404(Education, pk=pk)
    form = EducationForm(request.POST or None, instance=education)
    if form.is_valid():
        form.save()
        messages.success(request, 'Education updated.')
        return redirect('dashboard_educations')
    return render(request, 'dashboard/education_form.html', {
        'form': form, 'action': 'Edit', 'obj': education
    })


@login_required
@user_passes_test(superuser_check)
def delete_education_view(request, pk):
    education = get_object_or_404(Education, pk=pk)
    if request.method == 'POST':
        education.delete()
        messages.success(request, 'Education deleted.')
        return redirect('dashboard_educations')
    return render(request, 'dashboard/confirm_delete.html', {'obj': education, 'type': 'Education'})


# ── Contact Messages ──

@login_required
@user_passes_test(superuser_check)
def dashboard_messages_view(request):
    contact_messages = ContactMessage.objects.all()
    return render(request, 'dashboard/messages_list.html', {'contact_messages': contact_messages})


@login_required
@user_passes_test(superuser_check)
def mark_message_read_view(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.is_read = True
    msg.save()
    return redirect('dashboard_messages')
