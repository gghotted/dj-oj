from core.api.permissions import DjangoObjectPermissions, HasPerm
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.response import Response
from submissions.api.serializers import SubmissionSerializer
from submissions.models import Submission


class SubmissionDetailAPIView(RetrieveAPIView):
    permission_classes = [DjangoObjectPermissions]
    lookup_url_kwarg = 'submission_id'
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer


class SubmissionIsPublicToggleAPIView(GenericAPIView):
    permission_classes = [HasPerm('submissions.change_submission')]
    lookup_url_kwarg = 'submission_id'
    queryset = Submission.objects.all()
    
    def post(self, request, *args, **kwargs):
        submission = self.get_object()
        submission.is_public = not submission.is_public
        submission.save()

        if submission.is_public:
            message = '공개로 설정되었습니다'
        else:
            message = '비공개로 설정되었습니다'
        return Response({
            'message': message,
        })
