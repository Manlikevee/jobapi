from django.utils import timezone
from users.models import Profile


class UpdateLastSeenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            current_time = timezone.now()
            Profile.objects.update_or_create(
                user=request.user,
                defaults={'last_seen': current_time}
            )

        response = self.get_response(request)
        return response
