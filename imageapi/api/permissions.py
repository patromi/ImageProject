from rest_framework.permissions import BasePermission


class NormalPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.plan in ['BASIC','PREMIUM', 'ENTERPRISE', 'ROOT']

class PremiumPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.plan in ['PREMIUM', 'ENTERPRISE', 'ROOT']

class EnterprisePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.plan in ['ENTERPRISE', 'ROOT']

class RootPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.plan == 'ROOT'

class IsUploader(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.uploaded_by == request.user