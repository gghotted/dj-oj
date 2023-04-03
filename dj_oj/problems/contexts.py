from functools import cached_property

from core.contexts import Context
from django.urls import reverse


def navigation_list_problem():
    return (
        '문제 목록',
        '#',
    )


def navigation_list_solution(problem):
    return (
        '모든 풀이',
        reverse(
            'problems:list_solution',
            args=[problem.id]
        )
    )


class SolutionListContext(Context):
    keys = (
        # header
        'navigation',
        
        # contents
        'filter_form',
        'solutions',
        'page_obj',
    )

    def __init__(self, initial_ctx, request, problem, filter_form):
        super().__init__(initial_ctx, request)
        self.problem = problem
        self.filter_form = filter_form

    def navigation(self):
        from submissions.contexts import navigation_create_submission
        return [
            navigation_list_problem(),
            navigation_create_submission(self.problem, self.is_solved_problem),
            navigation_list_solution(self.problem)
        ]

    @cached_property
    def is_solved_problem(self):
        return (
            self.user.is_authenticated and
            self.problem.passed_users.filter(id=self.user.id).exists()
        )

    @cached_property
    def solutions(self):
        return list(self.initial_ctx['submission_list'])

    def page_obj(self):
        return self.initial_ctx['page_obj']
