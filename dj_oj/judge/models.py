from core.models import BaseModel
from django.db import models


class Judge(BaseModel):
    submission = models.OneToOneField(
        to='submissions.Submission',
        on_delete=models.CASCADE,
        related_name='judge',
        verbose_name='제출',
    )
    results_status = models.CharField(
        verbose_name='결과 상태',
        max_length=32,
        choices=[
            # python level
            ('success', '성공'),
            ('fail', '실패'),
            ('error', '에러'),

            # docker level
            ('error_timeout', '에러(시간초과)'),
            ('error_memory', '에러(메모리)'),
        ],
    )
    stderr = models.TextField(
        verbose_name='에러 출력',
        blank=True,
    )
    # 도커 run 부터 실행 시간
    runtime = models.FloatField(
        verbose_name='실행 시간',
        null=True,
    )
    test_total_count = models.PositiveIntegerField(
        verbose_name='테스트 총 개수',
        null=True,
    )
    test_passed_count = models.PositiveIntegerField(
        verbose_name='테스트 통과 개수',
        null=True,
    )


'''
정상 실행시(success or fail) result가 저장됨
'''
class TestResult(BaseModel):
    judge = models.ForeignKey(
        to=Judge,
        on_delete=models.CASCADE,
        related_name='test_results',
        verbose_name='judge',
    )
    number = models.PositiveIntegerField(
        verbose_name='번호',
    )
    runtime = models.FloatField(
        verbose_name='실행 시간',
    )
    status = models.CharField(
        verbose_name='결과 상태',
        max_length=32,
        choices=[
            ('success', '성공'),
            ('fail', '실패'),
            # ('error', '에러'), 한번에 실행되기 때문에 부분 에러는 없음
        ],
    )

    '''
    [
        {
            'time': float,
            'sql': str,
        }
    ]
    '''
    queries = models.JSONField(
        verbose_name='실행 쿼리',
        blank=True,
    )
    query_count = models.PositiveIntegerField(
        verbose_name='쿼리 갯수',
    )

    class Meta:
        ordering = ['number']

    @property
    def get_queries_display(self):
        fmt = (
            '--{time}ms ({i}/{total})\n'
            '{sql}'
        )
        total = len(self.queries)
        time_and_sqls = map(
            lambda t: fmt.format(**t[1], i=t[0], total=total),
            enumerate(self.queries, start=1)
        )
        contents = '\n\n'.join(time_and_sqls)
        title = '-- %d번 테스트의 SQL %d개' % (self.number, total)
        return title + '\n\n' + contents
