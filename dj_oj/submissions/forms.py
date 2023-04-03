import json

from django import forms
from django.forms import ValidationError

from submissions.models import Submission, SubmissionFile


class SubmissionCreateForm(forms.ModelForm):
    '''
    contents format
    {
        'file_name': 'contents',
    }
    '''
    contents = forms.JSONField()
    CONTENTS_MAX_LENGTH = 1024 * 16

    class Meta:
        model = Submission
        fields = (
            'contents',
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.problem = kwargs.pop('problem')
        self.editable_files = kwargs.pop('editable_files')

        if ('data' in kwargs and
            'contents' in kwargs['data']):
            contents = json.loads(kwargs['data']['contents'])
        else:
            contents = {}
        for file in self.editable_files:
            '''
            랜더링될 초기 contents 값은
            request data가 있다면 이 값으로,
            혹은 file의 기본 contents 값으로 한다.
            '''
            file.contents_for_editor = contents.get(file.name, file.contents)

        super().__init__(*args, **kwargs)

    def clean_contents(self):
        editable_names = set(map(
            lambda f: f.name,
            self.editable_files
        ))
        contents = self.cleaned_data.get('contents')
        submission_names = set(contents.keys())

        if editable_names != submission_names:
            raise ValidationError('제출 가능한 파일을 모두 제출해야합니다')

        for name, value in contents.items():
            if len(value) > self.CONTENTS_MAX_LENGTH:
                raise ValidationError('%s 파일의 데이터가 너무 큽니다' % name)
        
        return contents

    def save(self):
        total_contents_len = sum(
            len(self.cleaned_data['contents'][editable.name])
            for editable in self.editable_files
        )
        obj = Submission.objects.create(
            created_by=self.user,
            problem=self.problem,
            total_contents_len=total_contents_len,
        )
        files = [
            SubmissionFile(
                submission=obj,
                name=editable.name,
                path=editable.path,
                contents=self.cleaned_data['contents'][editable.name]
            )
            for editable in self.editable_files
        ]
        SubmissionFile.objects.bulk_create(files)
        return obj
