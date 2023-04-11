from categories.models import Category
from core.permissions import PermissionRequiredMixin
from django.db.models import Count, F, Prefetch
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from problems.contexts import ProblemListForAdminContext
from problems.models import Problem
from pure_pagination.mixins import PaginationMixin


class ProblemListForAdmin(
    PermissionRequiredMixin,
    PaginationMixin,
    ListView
):
    template_name = 'problems/admin/list.html'
    paginate_by = 10

    permission_required = 'problems.view_problem_list_for_admin'

    def get_queryset(self):
        qs = (
            Problem.objects.annotates(
                'passed_users_count',
            )
            .prefetch_related('categories')
            .order_by('-created_at')
        )
        try:
            categories = Category.tree.get_queryset_descendants(
                Category.objects.filter(id=self.request.GET['category']),
                include_self=True,
            )
            return qs.filter(skil_category__in=categories)
        except Exception:
            return qs

    def get_context_data(self, **kwargs):
        with_count = (
            Category.objects
            .annotate(
                children_problem_count=Count('children__problems', distinct=True),
                self_problem_count=Count('problems', distinct=True),
                problem_count=F('children_problem_count') + F('self_problem_count'),
            )
        )
        categories = (
            with_count.filter(level=0)
            .prefetch_related(Prefetch('children', with_count.all()))
        )
        return ProblemListForAdminContext(
            super().get_context_data(**kwargs),
            self.request,
            categories=categories
        ).to_dict()
