from django.urls import path
from submissions.views import SubmissionDetailView

app_name = 'submissions'

urlpatterns = [
    path('<int:submission_id>/', SubmissionDetailView.as_view(), name='detail'),
]
