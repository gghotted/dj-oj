from django.db.models.expressions import F, Window
from django.db.models.functions import window
from django.utils.formats import localize
from django.utils.timezone import localtime, now
from users.models import User

from ranks.models import Rank


def update_rank():
    users = list(
        User.objects.annotates('score', 'rank_val').select_related('rank')
    )

    for user in users:
        rank_obk = user.rank
        rank_obk.rank = user.rank_val
        rank_obk.score = user.score

    Rank.objects.bulk_update(
        map(lambda u: u.rank, users),
        ['rank', 'score'],
    )
    Rank.objects.update(updated_at=now())

    log = '%s: %d 개의 유저 랭크가 업데이트 되었습니다' % (
        localize(localtime(now())), len(users)
    )
    print(log)
