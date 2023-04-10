from django.urls import path

from submissions.views import SubmissionDetailView, SubmissionListView

app_name = 'submissions'

urlpatterns = [
    path('', SubmissionListView.as_view(), name='list'),
    path('<str:submission_uuid>/', SubmissionDetailView.as_view(), name='detail'),
]
