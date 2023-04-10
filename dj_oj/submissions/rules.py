from core.rules import pred_divide
from problems.rules import is_passed

import rules


@rules.predicate
def is_public(user, subm):
    return subm.is_public


@rules.predicate
def is_owner(user, subm):
    return subm.created_by == user


@rules.predicate
def test_completed(user, subm):
    return subm.test_status == 'completed'


@rules.predicate
def is_passed_problem(user, subm):
    return is_passed.test(user, subm.problem)


view_submission_from_list_obj = rules.is_authenticated & (
    is_owner | 
    (is_passed_problem & is_public)
)


rules.add_perm('submissions.view_submission', pred_divide(rules.always_true, is_public | is_owner))
rules.add_perm('submissions.change_submission', pred_divide(rules.is_authenticated, is_owner))
rules.add_perm('submissions.delete_submission', pred_divide(rules.is_authenticated, is_owner & test_completed))
rules.add_perm('submissions.react_submission', pred_divide(rules.is_authenticated, is_public | is_owner))
rules.add_perm('submissions.view_submission_from_list', pred_divide(rules.always_true, view_submission_from_list_obj))
