from django.urls import path
from submissions.api.views import (SubmissionDetailAPIView,
                                   SubmissionIsPublicToggleAPIView)

app_name = 'submissions_api'

urlpatterns = [
    path('<int:submission_id>/', SubmissionDetailAPIView.as_view(), name='detail'),
    path('<int:submission_id>/is-public-toggle/',
        SubmissionIsPublicToggleAPIView.as_view(),
        name='is_public_toggle',
    ),
]
