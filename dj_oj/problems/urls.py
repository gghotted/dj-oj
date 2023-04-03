from django.urls import path
from submissions.views import SubmissionCreateView

from problems.views.solution import SolutionListView

app_name = 'problems'

urlpatterns = [
    path(
        '<int:problem_id>/submissions/create/',
        SubmissionCreateView.as_view(),
        name='create_submission'
    ),
    path(
        '<int:problem_id>/solutions/',
        SolutionListView.as_view(),
        name='list_solution',
    )
]
