from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from problems.models import Problem

from submissions.forms import SubmissionCreateForm


@method_decorator(login_required, 'post')
class SubmissionCreateView(
    CreateView
):
    template_name = 'submissions/detail.html'
    form_class = SubmissionCreateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['problem'] = get_object_or_404(Problem, id=self.kwargs['problem_id'])
        kwargs['editable_files'] = kwargs['problem'].editable_files.all()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form = ctx['form']
        
        ctx['navigation'] = [
            ('문제 목록', '#'),
            (form.problem.title, self.request.path),
        ]
        ctx['can_read_another_solution'] = True # 수정해야함
        ctx['submissions'] = True # 수정해야함
        return ctx

    def form_invalid(self, form):
        messages.add_message(
            self.request,
            messages.ERROR,
            form.errors.render(),
        )
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('problems:create_submission', args=[self.object.problem.id])
