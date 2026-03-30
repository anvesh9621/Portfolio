from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.http import HttpResponse

def health_check(request):
    return HttpResponse("OK", content_type="text/plain", status=200)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check),
    path('', include('accounts_app.urls')),
    path('', include('projects_app.urls')),
    path('', include('skills_app.urls')),
    path('', include('achievements_app.urls')),
    path('', include('contact_app.urls')),
    path('api/', include('api_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
