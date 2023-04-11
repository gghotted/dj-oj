from core.fields import TemporaryZipFileField
from core.models import BaseModel
from django.conf import settings
from django.db import models
from tinymce.models import HTMLField

from problems import managers


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
        work_dir=settings.TEMP_DIR,
    )

    def __str__(self):
        return self.tag

    
class Category(BaseModel):
    name = models.CharField(
        verbose_name='이름',
        max_length=32,
    )
    display_name = models.CharField(
        verbose_name='보여지는 이름',
        max_length=32,
    )

    def __str__(self):
        return self.display_name


class Difficulty(BaseModel):
    name = models.CharField(
        verbose_name='이름',
        max_length=16,
    )
    display_name = models.CharField(
        verbose_name='보이는 이름',
        max_length=16,
    )
    score = models.PositiveIntegerField(
        verbose_name='점수',
    )

    def __str__(self):
        return self.display_name


class Problem(BaseModel):
    created_by = models.ForeignKey(
        to='users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_problems',
        verbose_name='생성자',
    )
    title = models.CharField(
        verbose_name='제목',
        max_length=64,
    )
    description = HTMLField()
    difficulty = models.ForeignKey(
        to=Difficulty,
        on_delete=models.SET_NULL,
        null=True,
        related_name='problems',
        verbose_name='난이도',
    )
    categories = models.ManyToManyField(
        to=Category,
        verbose_name='유형',
        related_name='problems',
    )
    base_docker_image = models.ForeignKey(
        to=DockerImage,
        on_delete=models.SET_NULL,
        null=True,
        related_name='problems',
        verbose_name='베이스 도커 이미지',
    )
    test_file = TemporaryZipFileField(
        verbose_name='zip 파일',
        upload_to='media/tests/',
        work_dir=settings.TEMP_DIR,
    )
    is_tested = models.BooleanField(
        verbose_name='테스트 여부',
        default=False,
    )
    number = models.PositiveIntegerField(
        verbose_name='번호',
        unique=True,
    )
    volume_tree = models.TextField(
        verbose_name='볼륨 트리 구조',
    )

    '''
    한 번 이라도 통과 했던 유저를 저장
    제출 기록을 삭제하더라도 통과 여부를 기록하기 위함
    '''
    passed_users = models.ManyToManyField(
        to='users.User',
        related_name='passed_problems',
        verbose_name='통과한 유저들',
        blank=True,
    )
    skil_category = models.ManyToManyField(
        to='categories.Category',
        related_name='problems',
        verbose_name='스킬 카테고리',
        blank=True,
    )

    objects = managers.ProblemManager()


class File(BaseModel):
    name = models.CharField(
        verbose_name='이름',
        max_length=64,
    )
    path = models.CharField(
        verbose_name='경로',
        max_length=255,
    )
    contents = models.TextField(
        verbose_name='내용',
    )

    class Meta(BaseModel.Meta):
        abstract = True
        ordering = ['name']


class EditableFile(File):
    problem = models.ForeignKey(
        to=Problem,
        on_delete=models.CASCADE,
        related_name='editable_files',
        verbose_name='문제',
    )
