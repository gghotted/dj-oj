from core.models import BaseManager
from django.db.models import Count


class SubmissionManager(BaseManager):

    def annotate_like_users_count(self, qs=None, user=None):
        qs = qs or self
        return qs.annotate(
            like_users_count=Count('like_users', distinct=True),
        )
