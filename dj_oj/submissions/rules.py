from core.rules import pred_divide

import rules


@rules.predicate
def is_public(user, subm):
    return subm.is_public


@rules.predicate
def is_owner(user, subm):
    return subm.created_by == user


rules.add_perm('submissions.view_submission', pred_divide(rules.always_true, is_public | is_owner))
rules.add_perm('submissions.change_submission', pred_divide(rules.is_authenticated, is_owner))
rules.add_perm('submissions.delete_submission', pred_divide(rules.is_authenticated, is_owner))
rules.add_perm('submissions.react_submission', pred_divide(rules.is_authenticated, is_public | is_owner))
