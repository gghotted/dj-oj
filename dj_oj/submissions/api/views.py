from core.api.permissions import DjangoObjectPermissions
from django.urls import reverse
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from submissions.api.serializers import (SubmissionSerializer,
                                         SubmissionUpdateSerializer)
from submissions.models import Submission


class SubmissionDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [DjangoObjectPermissions]
    lookup_url_kwarg = 'submission_uuid'
    lookup_field = 'uuid'

    queryset = Submission.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return SubmissionUpdateSerializer
        return SubmissionSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        redirect_url = reverse('problems:create_submission', args=[instance.problem.id])
        self.perform_destroy(instance)
        return Response({'redirect_url': redirect_url})
