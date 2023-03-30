from core.models import BaseModel
from django.db import models
from problems.models import File


class Submission(BaseModel):
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


class SubmissionFile(File):
    submission = models.ForeignKey(
        to=Submission,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='제출',
    )
