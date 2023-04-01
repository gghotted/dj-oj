import importlib.machinery
from time import time

import sqlparse
from docker.errors import ContainerError
from submissions.models import Submission

from judge.models import Judge, TestResult

ERR_RESULT_STATUS_MAP = {
    1: 'error',
    124: 'error_timeout',
    137: 'error_memory',
}


def pretty_sql(queries):
    for query in queries:
        raw = query['sql']
        statements = sqlparse.split(raw)
        formatted = [
            sqlparse.format(statement, reindent=True, keyword_case='upper')
            for statement in statements
        ]
        query['sql'] = '\n'.join(formatted)
    return queries


def save_test_result(judge, result_list):
    objs = []
    for result in result_list:
        obj = TestResult(
            judge=judge,
            number=result['number'],
            runtime=result['time'],
            status='success' if result['passed'] else 'fail',
            queries=pretty_sql(result['queries']),
            query_count=len(result['queries']),
        )
        objs.append(obj)
    return TestResult.objects.bulk_create(objs)


def _run_judge(judge, run_func, input_files, volume_path):
    start = time()

    result = None
    try:
        result = run_func(input_files, volume_path)
        judge.test_passed_count = sum(
            int(test['passed'])
            for test in result
        )
        judge.test_total_count = len(result)
        if judge.test_total_count == judge.test_passed_count:
            judge.results_status = 'success'
            judge.submission.problem.passed_users.add(judge.submission.created_by)
        else:
            judge.results_status = 'fail'

    except ContainerError as e:
        judge.results_status = ERR_RESULT_STATUS_MAP.get(e.exit_status, 'error')
        judge.stderr = e.stderr.decode('utf-8')
    except Exception as e:
        judge.results_status = 'error'
        judge.stderr = str(e)

    judge.runtime = (time() - start) * 1000
    judge.save()

    if result:
        save_test_result(judge, result)
    

def run_judge(submission_id):
    submission_qs = Submission.objects.filter(id=submission_id)
    submission = submission_qs.filter(judge__isnull=True).get(id=submission_id)
    problem = submission.problem

    submission_qs.update(test_status='in_progress')

    with problem.test_file.unzip() as path:
        test = importlib.machinery.SourceFileLoader(
            'test%d' % problem.number, str(path / 'test/__init__.py')
        ).load_module()

        input_files = {
            file.name: file.contents
            for file in submission.files.all()
        }
        volume_path = path / 'volume'
        judge = Judge(submission=submission)
        _run_judge(
            judge,
            test.run,
            input_files,
            volume_path
        )
    
    submission_qs.update(test_status='completed')
