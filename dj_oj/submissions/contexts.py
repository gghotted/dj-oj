from functools import cached_property

from core.contexts import Context
from django.urls import reverse
from problems.contexts import navigation_list_problem


def navigation_create_submission(problem, is_solved_problem):
    title = problem.title
    if is_solved_problem:
        title += '<span class="badge bg-success ms-1">&check;</span>'
    return (
        title,
        reverse(
            'problems:create_submission',
            args=[problem.id]
        )
    )


class SubmissionCreateContext(Context):
    keys = (
        # header
        'navigation',
        'is_solved_problem',

        # contents
        'problem',
        'initial_files',

        # footer
        'can_view_another_solution',
        'can_view_submissions',
        'submissions',
        'can_submit',
    )

    def __init__(self, initial_ctx, request, problem):
        super().__init__(initial_ctx, request)
        self.problem = problem

    def navigation(self):
        return [
            navigation_list_problem(),
            navigation_create_submission(self.problem, self.is_solved_problem)
        ]

    @cached_property
    def is_solved_problem(self):
        return (
            self.user.is_authenticated and
            self.problem.passed_users.filter(id=self.user.id).exists()
        )

    def initial_files(self):
        '''
        [
            {
                name: str,
                path: str,
                contents: str,
            }
        ]
        '''
        return [
            {
                'id': file.id,
                'name': file.name,
                'path': file.path,
                'contents': file.contents_for_editor,
            }
            for file in self.initial_ctx['form'].editable_files
        ]

    def can_view_another_solution(self):
        return self.is_solved_problem

    def can_view_submissions(self):
        return bool(self.submissions)
    
    @cached_property
    def submissions(self):
        if not self.user.is_authenticated:
            return []
        return list(self.user.submissions.filter(problem=self.problem))

    def can_submit(self):
        return self.user.has_perm('problems.add_submission', self.problem)
