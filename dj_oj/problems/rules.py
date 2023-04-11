from core.rules import pred_divide

import rules


@rules.predicate
def is_tested(user, problem):
    return problem.is_tested


@rules.predicate
def is_passed(user, problem):
    cache_name = '_passed_problems'

    if not hasattr(user, cache_name):
        setattr(user, cache_name, set())

    cached = getattr(user, cache_name)
    if problem.id in cached:
        return True

    if problem.passed_users.filter(id=user.id).exists():
        cached.add(problem.id)
        return True

    return False


rules.add_perm('problems.add_problem', rules.always_false)
rules.add_perm('problems.view_problem', pred_divide(rules.always_true, is_tested))
rules.add_perm('problems.chage_problem', rules.always_false)
rules.add_perm('problems.delete_problem', rules.always_false)
rules.add_perm('problems.add_submission', pred_divide(rules.is_authenticated, is_tested))
rules.add_perm('problems.view_solution', pred_divide(rules.is_authenticated, is_passed))
rules.add_perm('problems.view_problem_list_for_admin', rules.is_superuser),
