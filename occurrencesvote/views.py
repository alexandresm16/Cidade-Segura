from django.views.generic import CreateView, View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.urls import reverse_lazy
from .models import Occurrence, OccurrenceVote
from .forms import OccurrenceVoteForm


class OccurrenceVoteCreateView(LoginRequiredMixin, View):
    template_name = 'denuncia_lista.html'
    context_object_name = 'occurrences'
    success_message = 'Denúncia realizada com sucesso.'
    success_url = reverse_lazy('denuncias_pendentes')

    def post(self, request, *args, **kwargs):
        occurrence = get_object_or_404(Occurrence, pk=kwargs['pk'])

        form = OccurrenceVoteForm(request.POST)
        if not form.is_valid():
            return redirect('denuncias_pendentes')

        vote = form.save(commit=False)
        vote.user = request.user
        vote.occurrence = occurrence

        if request.user.is_staff:
            vote.weight = 3
        else:
            vote.weight = 1

        try:
            vote.save()
            occurrence.update_status_by_votes()
            # Aqui adicionamos a mensagem de sucesso
            messages.success(request, 'Voto registrado com sucesso!')
        except IntegrityError:
            messages.warning(request, 'Você já votou nesta ocorrência.')

        return redirect('denuncias_pendentes')
