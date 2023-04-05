from functools import cached_property

from core.contexts import Context
from django.conf import settings
from django.urls import reverse
from users.models import User


def navigation_list_problem():
    return (
        '문제 목록',
        reverse('problems:list'),
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
        'filtered_total_count',
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
        return self.user.has_perm('problems.view_solution', self.problem)

    @cached_property
    def filtered_total_count(self):
        return self.page_obj().paginator.object_list.count()

    @cached_property
    def solutions(self):
        return list(self.initial_ctx['submission_list'])

    def page_obj(self):
        return self.initial_ctx['page_obj']


class ProblemListContext(Context):
    keys = (
        # contents
        'filter_form',
        'filtered_total_count',
        'problems',
        'user_score',
        'page_obj',
    )

    def __init__(self, initial_ctx, request, filter_form):
        super().__init__(initial_ctx, request)
        self.filter_form = filter_form

    def problems(self):
        return list(self.initial_ctx['problem_list'])

    @cached_property
    def filtered_total_count(self):
        return self.page_obj().paginator.object_list.count()

    def page_obj(self):
        return self.initial_ctx['page_obj']

    @cached_property
    def user_score(self):
        '''
        {
            user: User,
            passed_problems_count: int,
            score: int,
            rank: int,
        }
        '''
        if not self.user.is_authenticated:
            return {}
        user = User.objects.annotates('score').get(id=self.user.id)
        return {
            'user': user,
            'passed_problems_count': user.passed_problems.count(),
            'score': user.score, # live score
            'rank': user.rank.rank, # saved rank
            'rank_updated_at': user.rank.updated_at,
            'rank_help_message': (
                '랭크는 %d분마다 업데이트 됩니다 (%s 에 업데이트 되었습니다)' % (
                    settings.RANK_UPDATE_CYCLE_MINUTE,
                    user.rank.updated_at_visible,
                )
            ),
        }
