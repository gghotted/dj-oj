from rest_framework.permissions import \
    DjangoObjectPermissions as _DjangoObjectPermissions


class DjangoObjectPermissions(_DjangoObjectPermissions):
    perms_map = dict(_DjangoObjectPermissions.perms_map)
    perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
