from accounts_app.models import Profile


def portfolio_profile(request):
    """Injects the portfolio Profile into all template contexts."""
    try:
        profile = Profile.objects.first()
    except Exception:
        profile = None
    return {'profile': profile}
