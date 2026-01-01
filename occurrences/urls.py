from django.urls import path
from .views import OccurrenceCreateView, reverse_geocode, OccurrenceDetailView, OccurrenceListView, OccurrenceDeleteView
from occurrencesvote.views import OccurrenceVoteCreateView

urlpatterns = [
    path('Denunciar', OccurrenceCreateView.as_view(), name='denunciar'),
    path('Denuncias', OccurrenceListView.as_view(), name='denuncias_pendentes'),
    path('Denuncia/<int:pk>/', OccurrenceDetailView.as_view(), name='denuncia_detalhes'),
    path('reverse-geocode/', reverse_geocode, name='reverse_geocode'),
    path('Denuncia/<int:pk>/vote/', OccurrenceVoteCreateView.as_view(), name='occurrence_vote'),
    path('Denuncia/<int:pk>/excluir', OccurrenceDeleteView.as_view(), name='occurrence_delete'),
]
