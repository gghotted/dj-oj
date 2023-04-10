from django.conf import settings


def version_hash(request):
    return {
        'version': settings.VERSION_HASH
    }
