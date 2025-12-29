from django.urls import path
from .views import OccurrenceCreateView, reverse_geocode, OccurrenceDetailView

urlpatterns = [
    path('Denunciar', OccurrenceCreateView.as_view(), name='denunciar'),
    path('Denuncia/<int:pk>/', OccurrenceDetailView.as_view(), name='denuncia_detalhes'),
    path('reverse-geocode/', reverse_geocode, name='reverse_geocode'),
]