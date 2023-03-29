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


class SubmissionFile(File):
    submission = models.ForeignKey(
        to=Submission,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='제출',
    )
