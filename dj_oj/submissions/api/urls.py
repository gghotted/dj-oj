from django.urls import path
from submissions.api.views import SubmissionDetailAPIView

app_name = 'submissions_api'

urlpatterns = [
    path('<int:submission_id>/', SubmissionDetailAPIView.as_view(), name='detail'),
]
