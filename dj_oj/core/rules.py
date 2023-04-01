import rules


def pred_divide(model_level_pred, object_level_pred):
    '''
    model level 에서의 권한
    object level 에서의 권한을 분리해서 관리
    '''
    @rules.predicate
    def wrapped(user, obj):
        if not obj:
            return model_level_pred.test(user, obj)
        else:
            return object_level_pred.test(user, obj)

    return wrapped
