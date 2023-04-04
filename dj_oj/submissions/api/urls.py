from django.urls import path
from submissions.api.views import (SubmissionDetailAPIView,
                                   SubmissionLikeAPIView,
                                   SubmissionUnLikeAPIView)

app_name = 'submissions_api'

urlpatterns = [
    path('<str:submission_uuid>/', SubmissionDetailAPIView.as_view(), name='detail'),
    path(
        '<str:submission_uuid>/like/',
        SubmissionLikeAPIView.as_view(),
        name='like',
    ),
    path(
        '<str:submission_uuid>/unlike/',
        SubmissionUnLikeAPIView.as_view(),
        name='unlike',
    )
]
