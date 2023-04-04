from core.models import BaseManager
from django.db.models import Count, Exists, OuterRef
from users.models import User


class ProblemManager(BaseManager):

    def annotate_passed_users_count(self, qs=None, user=None):
        qs = qs or self
        return qs.annotate(
            passed_users_count=Count('passed_users', distinct=True),
        )

    def annotate_is_solved(self, qs=None, user=None):
        if not user:
            raise Exception('user cannot be None')
        
        qs = qs or self
        return qs.annotate(is_solved=Exists(
            User.objects.filter(
                id=user.id,
                passed_problems__id=OuterRef('id')
            )
        ))
