from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('projects/', views.ProjectListCreateAPIView.as_view(), name='api_projects'),
    path('contact/', views.ContactCreateAPIView.as_view(), name='api_contact'),
    path('auth/token/', obtain_auth_token, name='api_token'),
]
