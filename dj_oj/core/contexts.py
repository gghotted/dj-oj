from django.http import HttpRequest
from django.urls import reverse
from django.utils.formats import localize
from django.utils.timezone import localtime


class Context:
    keys = tuple()

    def __init__(self, initial_ctx, request):
        self.initial_ctx = initial_ctx
        self.request: HttpRequest = request
        self.user = self.request.user

    def to_dict(self):
        ctx = dict(self.initial_ctx)
        for key in self.keys:
            ctx[key] = getattr(self, key)
        return ctx


def navigation(context: dict):
    problem = context.get('problem')
    submission = context.get('submission')

    navs = [
        ('문제 목록', '#'),
    ]

    if problem:
        title = problem.title
        if context.get('is_passed_user') == True:
            title += '<span class="badge bg-success ms-1">&check;</span>'
        navs.append((
            title,
            reverse(
                'problems:create_submission',
                args=[problem.id],
            )
        ))

    if submission:
        navs.append((
            '제출 결과(%s)' % localize(localtime(submission.created_at)),
            reverse(
                'submissions:detail',
                args=[submission.uuid]
            )
        ))
    
    return navs
