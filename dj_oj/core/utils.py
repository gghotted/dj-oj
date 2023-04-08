from django.conf import settings


def path_for_host(path):
    if not hasattr(settings, 'BASE_DIR_FROM_HOST'):
        return path
    
    base_dir_from_host = settings.BASE_DIR_FROM_HOST
    base_dir = settings.BASE_DIR
    relative = path.relative_to(base_dir)
    return base_dir_from_host / relative
