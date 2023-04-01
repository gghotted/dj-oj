from functools import cache

from braces.views import LoginRequiredMixin
from core.contexts import navigation
from core.permissions import PermissionRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.formats import localize
from django.utils.timezone import localtime
from django.views.generic import CreateView, DetailView
from problems.models import Problem

from submissions.contexts import (SubmissionCreateContext,
                                  SubmissionDetailContext)
from submissions.forms import SubmissionCreateForm
from submissions.models import Submission


@method_decorator(login_required, 'post')
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
        submission_id = self.request.GET.get('initial')

        if not submission_id:
            return problem.editable_files.all()
        
        submission = get_object_or_404(problem.submissions, id=submission_id)
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

    def form_invalid(self, form):
        messages.add_message(
            self.request,
            messages.ERROR,
            form.errors.render(),
        )
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('submissions:detail', args=[self.object.id])


class SubmissionDetailView(
    PermissionRequiredMixin,
    DetailView
):
    template_name = 'submissions/detail/detail.html'
    pk_url_kwarg = 'submission_id'
    queryset = Submission.objects.all()
    
    permission_required = 'submissions.view_submission'
    object_level_permissions = True

    def get_context_data(self, **kwargs):
        return SubmissionDetailContext(
            super().get_context_data(**kwargs),
            self.request,
            self.get_object(),
        ).to_dict()
