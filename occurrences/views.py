import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DetailView, ListView

from occurrencesvote.forms import OccurrenceVoteForm
from .models import Occurrence
from .forms import OccurrenceForm
from django.http import JsonResponse
from django.urls import reverse_lazy


class OccurrenceCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Occurrence
    form_class = OccurrenceForm
    template_name = 'denunciar.html'
    success_url = reverse_lazy('home')
    success_message = 'Denúncia realizada com sucesso.'
    login_url = 'login'  # nome da URL de login
    redirect_field_name = 'next'  # opcional (padrão)

    def form_valid(self, form):
        form.instance.reporter = self.request.user

        occurrence = form.save(commit=False)

        endereco = f"{occurrence.logradouro}, 0, {occurrence.bairro}, {occurrence.cidade}, {occurrence.uf}, Brasil"

        # URL da API do LocationIQ
        url = "https://us1.locationiq.com/v1/search"

        # Substitua com sua chave real
        API_KEY = 'pk.e03fb0df144869447ee210c6ba631214'

        params = {
            'key': API_KEY,
            'q': endereco,
            'format': 'json',
            'limit': 1
        }

        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()

            if data:
                occurrence.latitude = data[0].get('lat')
                occurrence.longitude = data[0].get('lon')

        except requests.RequestException as e:
            print(f"Erro ao buscar geolocalização: {e}")

        return super().form_valid(form)


def reverse_geocode(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    if not lat or not lon:
        return JsonResponse({'error': 'Latitude e longitude são obrigatórias'}, status=400)

    url = 'https://nominatim.openstreetmap.org/reverse'
    params = {
        'format': 'json',
        'lat': lat,
        'lon': lon,
        'addressdetails': 1,
    }

    headers = {
        'User-Agent': 'CidadeSegura/1.0 (contato@exemplo.com)'
    }

    response = requests.get(url, params=params, headers=headers, timeout=10)

    if response.status_code != 200:
        return JsonResponse({'error': 'Erro ao consultar o Nominatim'}, status=500)

    return JsonResponse(response.json())


class OccurrenceDetailView(DetailView):
    model = Occurrence
    template_name = 'denuncia_detalhes.html'
    context_object_name = 'occurrence'


class OccurrenceListView(LoginRequiredMixin, ListView):
    model = Occurrence
    template_name = 'denuncia_lista.html'
    context_object_name = 'occurrences'

    def get_queryset(self):
        user = self.request.user
        return Occurrence.objects.filter(status='pending') \
            .exclude(votes__user=user) \
            .exclude(reporter=user) \
            .order_by('created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vote_form'] = OccurrenceVoteForm()
        return context
