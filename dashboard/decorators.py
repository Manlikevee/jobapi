from rest_framework import permissions, status
from django.db.models import Q
from rest_framework.response import Response

from users.models import messagestarter


class LoanVerificationPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if messagestarter.objects.filter(Q(sender=request.user) | Q(reciever=request.user)).exists():
            return True
        else:
            return Response({'message': 'This keyword already exists'}, status=status.HTTP_400_BAD_REQUEST)


    def has_object_permission(self, request, view, obj):
        # You can implement object-level permissions here if needed
        return True