from django.urls import path

from submissions.views import SubmissionDetailView

app_name = 'submissions'

urlpatterns = [
    path('<str:submission_uuid>/', SubmissionDetailView.as_view(), name='detail'),
]
