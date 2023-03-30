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
