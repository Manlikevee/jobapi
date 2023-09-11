from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.utils import timezone


@receiver(user_logged_in)
def update_last_seen(sender, request, user, **kwargs):
    user.profile.last_seen = timezone.now()
    user.profile.save()