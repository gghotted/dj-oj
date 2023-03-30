from core.api.permissions import DjangoObjectPermissions
from rest_framework.generics import RetrieveAPIView
from submissions.api.serializers import SubmissionSerializer
from submissions.models import Submission


class SubmissionDetailAPIView(RetrieveAPIView):
    permission_classes = [DjangoObjectPermissions]
    lookup_url_kwarg = 'submission_id'
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
