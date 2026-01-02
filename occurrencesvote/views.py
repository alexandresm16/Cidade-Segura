from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.urls import reverse_lazy

from .models import Occurrence, OccurrenceVote
from .forms import OccurrenceVoteForm


class OccurrenceVoteCreateView(LoginRequiredMixin, View):
    template_name = 'denuncia_lista.html'
    success_url = reverse_lazy('denuncias_pendentes')

    def get(self, request, *args, **kwargs):
        occurrences = Occurrence.objects.filter(status='pending')

        for occurrence in occurrences:
            occurrence.vote_form = OccurrenceVoteForm()

        return render(request, self.template_name, {
            'occurrences': occurrences,
        })

    def post(self, request, *args, **kwargs):
        occurrence = get_object_or_404(Occurrence, pk=kwargs['pk'])
        form = OccurrenceVoteForm(request.POST)

        if not form.is_valid():
            messages.error(request, 'Selecione uma opção válida.')
            return redirect(self.success_url)

        vote = form.save(commit=False)
        vote.user = request.user
        vote.occurrence = occurrence
        vote.weight = 3 if request.user.is_staff else 1

        try:
            vote.save()
            occurrence.update_status_by_votes()
            messages.success(request, 'Voto registrado com sucesso!')
        except IntegrityError:
            messages.warning(request, 'Você já votou nesta ocorrência.')

        return redirect(self.success_url)
