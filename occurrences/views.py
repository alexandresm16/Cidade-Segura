from django.shortcuts import render
import requests
from django.views.generic import CreateView
from .models import Occurrence
from .forms import OccurrenceForm
from django.http import JsonResponse
from django.urls import reverse_lazy


class OccurrenceCreateView(CreateView):
    model = Occurrence
    form_class = OccurrenceForm
    template_name = 'denunciar.html'
    success_url = reverse_lazy('/')
    success_message = 'Denuncia realizada com sucesso.'

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.reporter = self.request.user

            occurrence = form.save(commit=False)
            # Montar endereço para geocoding
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
                    resultado = data[0]
                    occurrence.latitude = resultado.get('lat')
                    occurrence.longitude = resultado.get('lon')
                else:
                    occurrence.latitude = None
                    occurrence.longitude = None

            except (requests.RequestException, KeyError, IndexError) as e:
                # Log de erro
                print(f"Erro ao buscar geolocalização: {e}")
                occurrence.latitude = None
                occurrence.longitude = None

            occurrence.save()
            return super().form_valid(form)
        else:
            print("Não está logado!!!")


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
