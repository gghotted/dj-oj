from rest_framework.permissions import BasePermission
from rest_framework.permissions import \
    DjangoObjectPermissions as _DjangoObjectPermissions


class DjangoObjectPermissions(_DjangoObjectPermissions):
    perms_map = dict(_DjangoObjectPermissions.perms_map)
    perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


class CallbleMixin:
    
    def __call__(self):
        return self


class HasPerm(CallbleMixin, BasePermission):

    def __init__(self, perm):
        self.perm = perm

    def has_permission(self, request, view):
        return request.user.has_perm(self.perm)

    def has_object_permission(self, request, view, obj):
        return request.user.has_perm(self.perm, obj)
