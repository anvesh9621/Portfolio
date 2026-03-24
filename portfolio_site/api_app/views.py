from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings as django_settings

from projects_app.models import Project
from contact_app.models import ContactMessage
from .serializers import ProjectSerializer, ContactMessageSerializer


class ProjectListCreateAPIView(generics.ListCreateAPIView):
    """
    GET  /api/projects/  — Returns all projects (public)
    POST /api/projects/  — Create new project (token auth required)
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class ContactCreateAPIView(generics.CreateAPIView):
    """
    POST /api/contact/  — Submit contact message (public)
    Saves to DB and sends emails.
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact = serializer.save()

        # Send emails
        try:
            send_mail(
                subject=f'New API Contact from {contact.name}',
                message=f'Name: {contact.name}\nEmail: {contact.email}\n\nMessage:\n{contact.message}',
                from_email=django_settings.DEFAULT_FROM_EMAIL,
                recipient_list=[django_settings.ADMIN_EMAIL],
                fail_silently=True,
            )
            send_mail(
                subject='Thank you for reaching out!',
                message=(
                    f'Hi {contact.name},\n\nThank you for your message! '
                    'I will get back to you shortly.\n\nBest regards,'
                ),
                from_email=django_settings.DEFAULT_FROM_EMAIL,
                recipient_list=[contact.email],
                fail_silently=True,
            )
        except Exception:
            pass

        headers = self.get_success_headers(serializer.data)
        return Response(
            {'message': 'Your message has been sent!', 'data': serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
