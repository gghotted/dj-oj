from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User

from ranks.models import Rank


@receiver(post_save, sender=User)
def create_rank(sender, instance, *args, **kwargs):
    if not kwargs['created']:
        return
    
    Rank.objects.create(user=instance)
