from core.models import BaseManager
from django.db.models import Count, Exists, OuterRef
from users.models import User


class SubmissionManager(BaseManager):

    def annotate_like_users_count(self, qs=None, user=None):
        qs = qs or self
        return qs.annotate(
            like_users_count=Count('like_users', distinct=True),
        )

    def annotate_is_liked_by_user(self, qs=None, user=None):
        self.check_required_user(user)

        qs = qs or self
        return qs.annotate(
            is_liked_by_user=Exists(
                User.objects.filter(like_submissions__id=OuterRef('id'))
            )
        )
