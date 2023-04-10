from functools import cache

import django_filters
from core.permissions import PermissionRequiredMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.forms import widgets
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView
from django_ratelimit.decorators import ratelimit
from judge.tasks import run_judge
from problems.models import Problem
from pure_pagination.mixins import PaginationMixin

from submissions.contexts import (SubmissionCreateContext,
                                  SubmissionDetailContext,
                                  SubmissionListContext)
from submissions.forms import SubmissionCreateForm
from submissions.models import Submission


def get_limit_rate_submission_create(group, request):
    if request.user.is_superuser:
        request.user._ratelimit_exception_context = {
            'message': '분당 100개의 제출 제한이 있습니다'
        }
        return '100/m'
    else:
        request.user._ratelimit_exception_context = {
            'message': '분당 5개의 제출 제한이 있습니다'
        }
        return '5/m'


@method_decorator(ratelimit(key='user', rate=get_limit_rate_submission_create), 'post')
class SubmissionCreateView(
    PermissionRequiredMixin,
    CreateView
):
    template_name = 'submissions/create/create.html'
    form_class = SubmissionCreateForm
    pk_url_kwarg = 'problem_id'

    object_level_permissions = True

    @cache
    def get_object(self, queryset=None):
        return get_object_or_404(Problem, id=self.kwargs['problem_id'])

    def get_permission_required(self, request=None):
        if request.method == 'GET':
            return 'problems.view_problem'
        else:
            return 'problems.add_submission'

    def get_editable_files(self, problem):
        submission_uuid = self.request.GET.get('initial')

        if not submission_uuid:
            return problem.editable_files.all()
        
        submission = get_object_or_404(problem.submissions, uuid=submission_uuid)
        if not self.request.user.has_perm('submissions.view_submission', submission):
            raise PermissionDenied
        
        return submission.files.all()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['problem'] = self.get_object()
        kwargs['editable_files'] = self.get_editable_files(kwargs['problem'])
        return kwargs

    def get_context_data(self, **kwargs):
        return SubmissionCreateContext(
            super().get_context_data(**kwargs),
            self.request,
            self.get_object(),
        ).to_dict()

    def form_valid(self, form):
        ret = super().form_valid(form)
        run_judge.delay(submission_id=self.object.id)
        return ret

    def form_invalid(self, form):
        messages.add_message(
            self.request,
            messages.ERROR,
            form.errors.render(),
        )
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('submissions:detail', args=[self.object.uuid])


class SubmissionDetailView(
    PermissionRequiredMixin,
    DetailView
):
    template_name = 'submissions/detail/detail.html'
    slug_url_kwarg = 'submission_uuid'
    slug_field = 'uuid'
    
    permission_required = 'submissions.view_submission'
    object_level_permissions = True

    def get_queryset(self):
        qs = (
            Submission.objects
            .annotates('like_users_count', 'is_liked_by_user', user=self.request.user)
        )
        return qs

    def get_context_data(self, **kwargs):
        return SubmissionDetailContext(
            super().get_context_data(**kwargs),
            self.request,
            self.get_object(),
        ).to_dict()


class SubmissionFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(
        widget=widgets.TextInput(attrs={'placeholder': '유저'}),
        field_name='created_by__nickname',
        lookup_expr='icontains',
        label='유저',
    )

    class Meta:
        model = Submission
        fields = (
            'user',
        )


class SubmissionListView(
    PermissionRequiredMixin,
    PaginationMixin,
    ListView
):
    template_name = 'submissions/list.html'
    paginate_by = 10

    permission_required = 'submissions.view_submission_from_list'

    def get_queryset(self):
        qs = Submission.objects.filter(
            created_by__is_superuser=False,
        )
        self.filter = SubmissionFilter(
            self.request.GET,
            queryset=qs,
        )
        return self.filter.qs

    def get_context_data(self, **kwargs):
        return SubmissionListContext(
            super().get_context_data(**kwargs),
            self.request,
            self.filter.form,
        ).to_dict()
