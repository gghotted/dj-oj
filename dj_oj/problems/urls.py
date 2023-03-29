from django.urls import path
from submissions.views import SubmissionCreateView

app_name = 'problems'

urlpatterns = [
    path(
        '<int:problem_id>/submissions/create/',
        SubmissionCreateView.as_view(),
        name='create_submission'
    ),
]
