from functools import cached_property

from core.contexts import Context
from django.urls import reverse
from django.utils.formats import localize
from django.utils.timezone import localtime
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


def navigation_detail_submission(submission):
    return (
        '%s 님의 제출(%s)' % (
            submission.created_by,
            localize(localtime(submission.created_at))
        ),
        reverse(
            'submissions:detail',
            args=[submission.uuid],
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


class SubmissionDetailContext(Context):
    keys = (
        # header
        'navigation',
        'is_solved_problem',
        'can_change_submission',

        # contents
        'submission',
        'files',
        'editor_readonly',

        # footer
        'can_delete_submission',
        'can_view_another_solution',
        'can_view_submissions',
        'submissions',
        'can_view_problem',
    )

    def __init__(self, initial_ctx, request, submission):
        super().__init__(initial_ctx, request)
        self.submission = submission
        self.problem = self.submission.problem
    
    def navigation(self):
        return [
            navigation_list_problem(),
            navigation_create_submission(self.problem, self.is_solved_problem),
            navigation_detail_submission(self.submission)
        ]

    @cached_property
    def is_solved_problem(self):
        return (
            self.user.is_authenticated and
            self.problem.passed_users.filter(id=self.user.id).exists()
        )

    def can_change_submission(self):
        return self.user.has_perm('submissions.change_submission', self.submission)

    @cached_property
    def files(self):
        return list(self.submission.files.all())

    def editor_readonly(self):
        return True

    def can_delete_submission(self):
        return self.user.has_perm('submissions.delete_submission', self.submission)

    def can_view_another_solution(self):
        return self.is_solved_problem
    
    def can_view_submissions(self):
        return bool(self.submissions)
    
    @cached_property
    def submissions(self):
        if not self.user.is_authenticated:
            return []
        return list(self.user.submissions.filter(problem=self.problem))
    
    def can_view_problem(self):
        return self.user.has_perm('problems.view_problem', self.problem)
