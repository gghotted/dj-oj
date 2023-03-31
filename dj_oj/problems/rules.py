from core.rules import pred_divide

import rules


@rules.predicate
def is_tested(user, problem):
    return problem.is_tested


rules.add_perm('problems.add_problem', rules.always_false)
rules.add_perm('problems.view_problem', pred_divide(rules.always_true, is_tested))
rules.add_perm('problems.chage_problem', rules.always_false)
rules.add_perm('problems.delete_problem', rules.always_false)
rules.add_perm('problems.add_submssion', pred_divide(rules.always_true, is_tested))
