import rules


def pred_divide(model_level_pred, object_level_pred):
    '''
    model level 에서의 권한 (볼수 있는 객체가 있을 수 있는가?)
        - 로그인 비로그인
            x    x     => always_false
            o    x     => is_authenticated
            o    O     => always_true

    object level 에서의 권한을 분리해서 관리 (이 객채를 볼 수 있는가?)
    '''
    @rules.predicate
    def wrapped(user, obj):
        if not obj:
            return model_level_pred.test(user, obj)
        else:
            return model_level_pred.test(user, obj) and object_level_pred.test(user, obj)

    return wrapped
