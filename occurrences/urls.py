from django.urls import path
from .views import OccurrenceCreateView, reverse_geocode

urlpatterns = [
    path('Denunciar', OccurrenceCreateView.as_view(), name='denunciar'),
    path('reverse-geocode/', reverse_geocode, name='reverse_geocode'),
]