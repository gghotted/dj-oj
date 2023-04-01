from rest_framework import serializers
from submissions.models import Submission


class SubmissionSerializer(serializers.ModelSerializer):
    test_status_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Submission
        fields = (
            'id',
            'test_status',
            'test_status_display',
        )

    def get_test_status_display(self, obj):
        return obj.get_test_status_display()


class SubmissionUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Submission
        fields = (
            'is_public',
        )

    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #     if instance.is_public:
    #         ret['message'] = '공개로 설정되었습니다'
    #     else:
    #         ret['message'] = '비공개로 설정되었습니다'
    #     return ret
