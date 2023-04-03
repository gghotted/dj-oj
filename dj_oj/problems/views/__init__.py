import django_filters
from core.permissions import PermissionRequiredMixin
from django.db.models.aggregates import Count
from django.db.models.expressions import Exists, OuterRef
from django.views.generic import ListView
from problems.contexts import ProblemListContext
from problems.models import Problem
from pure_pagination.mixins import PaginationMixin
from users.models import User


class ProblemFilter(django_filters.FilterSet):
    state = django_filters.ChoiceFilter(
        field_name='is_solved',
        choices=(
            (True, '푼 문제'),
            (False, '안 푼 문제'),
        ),
        label='상태'
    )
    o = django_filters.OrderingFilter(
        choices=(
            ('-created_at', '최신'),
            ('-passed_users_count', '푼 사람 많은'),
            ('passed_users_count', '푼 사람 적은'),
        ),
        label='정렬'
    )

    class Meta:
        model = Problem
        fields = (
            'difficulty',
            'state',
            'o',
        )


class ProblemListView(
    PermissionRequiredMixin,
    PaginationMixin,
    ListView
):
    template_name = 'problems/list.html'
    queryset = Problem.objects.all()
    paginate_by = 1

    permission_required = 'problems.view_problem'

    def get_queryset(self):
        qs = (
            Problem.objects.filter(is_tested=True)
            .annotate(passed_users_count=Count('passed_users', distinct=True))
            .annotate(is_solved=Exists(
                User.objects.filter(
                    id=self.request.user.id,
                    passed_problems__id=OuterRef('id')
                )
            ))
            .prefetch_related('categories')
            .order_by('-created_at') # annotate후 기본 order가 초기화됨
        )
        self.filter = ProblemFilter(
            self.request.GET,
            queryset=qs,
        )
        return self.filter.qs

    def get_context_data(self, **kwargs):
        return ProblemListContext(
            super().get_context_data(**kwargs),
            self.request,
            self.filter.form,
        ).to_dict()
