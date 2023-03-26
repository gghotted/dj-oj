from core.fields import TemporaryZipFileField
from core.models import BaseModel
from django.db import models


class DockerImage(BaseModel):
    tag = models.CharField(
        verbose_name='태그',
        unique=True,
        max_length=32,
    )
    zip_file = TemporaryZipFileField(
        verbose_name='zip 파일',
        upload_to='media/docker_images/',
        help_text='루트 폴더에 Dockerfile을 포함해야합니다',
    )

    def __str__(self):
        return self.tag
