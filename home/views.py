from django.shortcuts import render
from django.views.generic import TemplateView

from occurrences.models import Occurrence


# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pegando apenas ocorrências pendentes
        context['occurrences'] = Occurrence.objects.order_by('created_at')
        return context