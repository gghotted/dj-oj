from core.api.permissions import DjangoObjectPermissions, HasPerm
from django.urls import reverse
from rest_framework.generics import (GenericAPIView,
                                     RetrieveUpdateDestroyAPIView)
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


class SubmissionReactAPIView(GenericAPIView):
    permission_classes = [HasPerm('submissions.react_submission')]
    lookup_url_kwarg = 'submission_uuid'
    lookup_field = 'uuid'

    queryset = Submission.objects.all()

    success_message = 'success react'

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        self.perform_react(obj)
        return Response({'message': self.success_message})

    def perform_react(self, obj):
        raise NotImplementedError


class SubmissionLikeAPIView(SubmissionReactAPIView):
    success_message = 'set liked'

    def perform_react(self, obj):
        obj.like_users.add(self.request.user)


class SubmissionUnLikeAPIView(SubmissionReactAPIView):
    success_message = 'set unliked'

    def perform_react(self, obj):
        obj.like_users.remove(self.request.user)
