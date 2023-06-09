from functools import cached_property
from urllib.parse import urljoin, urlparse

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


def navigation_detail_submission(submission):
    return (
        '%s 님의 제출(%s)' % (
            submission.created_by,
            submission.created_at_relative,
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
        'can_view_solution',
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
        return self.user.has_perm('problems.view_solution', self.problem)

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

    def can_view_solution(self):
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
        'can_react_submission',
        'like_users_count',
        'is_liked_submission',
        'can_change_submission',

        # contents
        'submission',
        'files',
        'editor_readonly',

        # footer
        'can_delete_submission',
        'can_view_solution',
        'from_solutions_page', # solution 목록 페이지에서 왔는지 여부
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
        return self.user.has_perm('problems.view_solution', self.problem)

    @cached_property
    def can_react_submission(self):
        return self.user.has_perm('submissions.react_submission', self.submission)

    @cached_property
    def like_users_count(self):
        return self.submission.like_users_count

    @cached_property
    def is_liked_submission(self):
        return self.submission.is_liked_by_user

    @cached_property
    def can_change_submission(self):
        return self.user.has_perm('submissions.change_submission', self.submission)

    @cached_property
    def files(self):
        return list(self.submission.files.all())

    def editor_readonly(self):
        return True

    def can_delete_submission(self):
        return self.user.has_perm('submissions.delete_submission', self.submission)

    def can_view_solution(self):
        return self.is_solved_problem

    def from_solutions_page(self):
        solution_page = (
            self.request._current_scheme_host +
            reverse('problems:list_solution', args=[self.problem.id])
        )
        previouse_page = self.request.META.get('HTTP_REFERER')
        previouse_page = urljoin(
            previouse_page,
            urlparse(previouse_page).path,
        )
        return previouse_page == solution_page
    
    def can_view_submissions(self):
        return bool(self.submissions)
    
    @cached_property
    def submissions(self):
        if not self.user.is_authenticated:
            return []
        return list(self.user.submissions.filter(problem=self.problem))
    
    def can_view_problem(self):
        return self.user.has_perm('problems.view_problem', self.problem)


class SubmissionListContext(Context):
    keys = (
        # contents
        'filter_form',
        'filtered_total_count',
        'submissions',
        'page_obj',
    )

    def __init__(self, initial_ctx, request, filter_form):
        super().__init__(initial_ctx, request)
        self.filter_form = filter_form

    @cached_property
    def submissions(self):
        submissions = list(self.initial_ctx['submission_list'])
        for submission in submissions:
            submission.can_view = self.user.has_perm(
                'submissions.view_submission_from_list',
                submission,
            )
            submission.problem.can_view = self.user.has_perm(
                'problems.view_problem',
                submission.problem,
            )
        return submissions
    
    @cached_property
    def filtered_total_count(self):
        return self.page_obj().paginator.object_list.count()
    
    def page_obj(self):
        return self.initial_ctx['page_obj']
