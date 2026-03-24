from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard home
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Profile
    path('dashboard/profile/edit/', views.profile_edit_view, name='profile_edit'),

    # Projects CRUD
    path('dashboard/projects/', views.dashboard_projects_view, name='dashboard_projects'),
    path('dashboard/projects/add/', views.add_project_view, name='add_project'),
    path('dashboard/projects/<int:pk>/edit/', views.edit_project_view, name='edit_project'),
    path('dashboard/projects/<int:pk>/delete/', views.delete_project_view, name='delete_project'),
    path('dashboard/projects/<int:pk>/toggle/', views.toggle_featured_view, name='toggle_featured'),

    # Skills & Categories CRUD
    path('dashboard/skills/', views.dashboard_skills_view, name='dashboard_skills'),
    
    # Category endpoints
    path('dashboard/skills/category/add/', views.add_skill_category_view, name='add_skill_category'),
    path('dashboard/skills/category/<int:pk>/edit/', views.edit_skill_category_view, name='edit_skill_category'),
    path('dashboard/skills/category/<int:pk>/delete/', views.delete_skill_category_view, name='delete_skill_category'),
    
    # Skill endpoints (nested under nested categories)
    path('dashboard/skills/category/<int:category_id>/skill/add/', views.add_skill_view, name='add_skill'),
    path('dashboard/skills/skill/<int:pk>/edit/', views.edit_skill_view, name='edit_skill'),
    path('dashboard/skills/skill/<int:pk>/delete/', views.delete_skill_view, name='delete_skill'),

    # Achievements CRUD
    path('dashboard/achievements/', views.dashboard_achievements_view, name='dashboard_achievements'),
    path('dashboard/achievements/add/', views.add_achievement_view, name='add_achievement'),
    path('dashboard/achievements/<int:pk>/edit/', views.edit_achievement_view, name='edit_achievement'),
    path('dashboard/achievements/<int:pk>/delete/', views.delete_achievement_view, name='delete_achievement'),

    # Education CRUD
    path('dashboard/education/', views.dashboard_educations_view, name='dashboard_educations'),
    path('dashboard/education/add/', views.add_education_view, name='add_education'),
    path('dashboard/education/<int:pk>/edit/', views.edit_education_view, name='edit_education'),
    path('dashboard/education/<int:pk>/delete/', views.delete_education_view, name='delete_education'),

    # Messages
    path('dashboard/messages/', views.dashboard_messages_view, name='dashboard_messages'),
    path('dashboard/messages/<int:pk>/read/', views.mark_message_read_view, name='mark_message_read'),
]
