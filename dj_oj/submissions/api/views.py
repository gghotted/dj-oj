from core.api.permissions import DjangoObjectPermissions
from rest_framework.generics import (RetrieveAPIView, RetrieveUpdateAPIView,
                                     UpdateAPIView)
from submissions.api.serializers import (SubmissionSerializer,
                                         SubmissionUpdateSerializer)
from submissions.models import Submission


class SubmissionDetailAPIView(RetrieveUpdateAPIView):
    permission_classes = [DjangoObjectPermissions]
    lookup_url_kwarg = 'submission_id'
    queryset = Submission.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return SubmissionUpdateSerializer
        return SubmissionSerializer
