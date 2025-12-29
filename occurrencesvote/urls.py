from django.urls import path

from occurrencesvote.views import OccurrenceVoteCreateView

urlpatterns = [
    path('<int:pk>/vote/', OccurrenceVoteCreateView.as_view(), name='occurrence_vote'),
]
