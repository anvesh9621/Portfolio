from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings as django_settings
from .models import ContactMessage
from accounts_app.models import Profile


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        if not name or not email or not message:
            messages.error(request, 'All fields are required.')
            return redirect('contact')

        # Save to database
        ContactMessage.objects.create(name=name, email=email, message=message)

        # Send admin notification email
        try:
            send_mail(
                subject=f'New Contact Message from {name}',
                message=f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}',
                from_email=django_settings.DEFAULT_FROM_EMAIL,
                recipient_list=[django_settings.ADMIN_EMAIL],
                fail_silently=True,
            )

            # Send confirmation to user
            send_mail(
                subject='Thank you for reaching out!',
                message=(
                    f'Hi {name},\n\n'
                    'Thank you for your message! I have received it and will get back to you shortly.\n\n'
                    'Best regards,\nAnvesh Pandey'
                ),
                from_email=django_settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=True,
            )
        except Exception:
            pass  # Email failure shouldn't block the user

        messages.success(request, 'Your message has been sent! I will get back to you soon.')
        return redirect('contact')

    return render(request, 'contact.html')
