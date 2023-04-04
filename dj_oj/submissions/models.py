from core.models import BaseModel
from django.db import models
from django_extensions.db.fields import RandomCharField
from problems.models import File

from submissions import managers


class Submission(BaseModel):
    uuid = RandomCharField(
        verbose_name='uuid',
        length=12,
        unique=True,
    )
    created_by = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name='생성자',
    )
    problem = models.ForeignKey(
        to='problems.Problem',
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name='문제',
    )
    is_public = models.BooleanField(
        verbose_name='공개',
        default=False,
    )
    test_status = models.CharField(
        verbose_name='상태',
        max_length=32,
        choices=[
            ('pending', '대기중'),
            ('in_progress', '진행중'),
            ('completed', '완료'),
        ],
        default='pending',
    )
    total_contents_len = models.PositiveIntegerField(
        verbose_name='제출 파일의 총 길이',
    )
    like_users = models.ManyToManyField(
        to='users.User',
        related_name='like_submissions',
        verbose_name='좋아요한 유저들',
    )

    objects = managers.SubmissionManager()

    @property
    def get_test_status_detail_display(self):
        if self.test_status != 'completed':
            return self.get_test_status_display()
        if not self.judge.test_total_count:
            return self.judge.get_results_status_display()
        counts = '(%d/%d)' % (
            self.judge.test_passed_count,
            self.judge.test_total_count,
        )
        return self.judge.get_results_status_display() + counts


class SubmissionFile(File):
    submission = models.ForeignKey(
        to=Submission,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='제출',
    )
