from functools import cached_property

import django_filters
from core.permissions import PermissionRequiredMixin
from django.db.models.expressions import Q
from django.forms import widgets
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from problems.contexts import SolutionListContext
from problems.models import Problem
from pure_pagination.mixins import PaginationMixin
from submissions.models import Submission


class SolutionFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(
        widget=widgets.TextInput(attrs={'placeholder': '유저 이메일'}),
        field_name='created_by__email',
        lookup_expr='icontains',
        label='',
    )
    o = django_filters.OrderingFilter(
        choices=(
            ('-like_users_count', '좋아요 많은 순'),
            ('total_contents_len', '짧은 코드 순'),
            ('judge__average_query_count', '낮은 평균 쿼리 순'),
        ),
        empty_label='최신 순',
        label='',
    )

    class Meta:
        model = Submission
        fields = (
            'o',
            'user',
        )


class SolutionListView(
    PermissionRequiredMixin,
    PaginationMixin,
    ListView
):
    template_name = 'problems/solution/list.html'
    paginate_by = 15

    permission_required = 'problems.view_solution'
    object_level_permissions = True

    def get_object(self):
        return self.problem

    @cached_property
    def problem(self):
        return get_object_or_404(Problem, id=self.kwargs['problem_id'])

    def get_queryset(self):
        qs = (
            Submission.objects
            .annotates('like_users_count')
            .filter(problem=self.problem, judge__results_status='success')
            .filter(Q(is_public=True) | Q(created_by=self.request.user))
            .order_by('-created_at')
        )
        self.filter = SolutionFilter(self.request.GET, queryset=qs)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        return SolutionListContext(
            super().get_context_data(**kwargs),
            self.request,
            self.problem,
            self.filter.form,
        ).to_dict()
