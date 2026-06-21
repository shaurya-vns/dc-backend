from rest_framework.permissions import BasePermission
import json

class IsAdminUser(BasePermission):
    def has_permission(self, request):
        print('SSS '+json(request))
        return True