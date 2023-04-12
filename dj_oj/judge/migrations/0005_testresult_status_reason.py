# Generated by Django 4.1.7 on 2023-04-12 03:15

from django.db import migrations, models


def set_fail_reason(apps, _):
    TestResult = apps.get_model('judge', 'TestResult')
    for test in TestResult.objects.filter(status='fail'):
        test.status_reason = '결과 불일치'
        test.save()


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0004_judge_average_query_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='testresult',
            name='status_reason',
            field=models.CharField(blank=True, max_length=255, verbose_name='이유'),
        ),
        migrations.RunPython(
            set_fail_reason,
            lambda a, _: None,
        )
    ]
