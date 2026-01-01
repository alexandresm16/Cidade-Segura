from datetime import timedelta

from django.utils import timezone
from django.views.generic import TemplateView
import requests
from home.models import Weather
from occurrences.models import Occurrence

API_KEY = "caac1fc2ee9180b515b463db6781d518"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['occurrences'] = Occurrence.objects.order_by('created_at')

        clima = Weather.objects.last()
        context['data'] = timezone.now()

        # Atualiza apenas se não existir ou estiver desatualizado (>= 1 hora)
        if not clima or timezone.now() - clima.created_at >= timedelta(hours=1):
            novo_clima = fetch_and_save_weather()
            if novo_clima:
                clima = novo_clima  # só sobrescreve se deu certo

        context['clima'] = clima
        return context


def fetch_and_save_weather():
    params = {
        "lat": "-29.6914",
        "lon": "-53.8008",
        "appid": API_KEY,
        "units": "metric",
        "lang": "pt_br",
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)

        # Se a API respondeu com erro
        if response.status_code != 200:
            return None

        data = response.json()

        # Validação básica do retorno
        if (
                "main" not in data
                or "weather" not in data
                or not data["weather"]
        ):
            return None

        weather, _ = Weather.objects.update_or_create(
            city=data.get("name", "Desconhecido"),
            defaults={
                "temperature": data["main"].get("temp"),
                "description": data["weather"][0].get("description", ""),
                "humidity": data["main"].get("humidity"),
            },
        )

        return weather

    except (requests.exceptions.RequestException, ValueError):
        # Qualquer erro de rede ou JSON inválido
        return None
