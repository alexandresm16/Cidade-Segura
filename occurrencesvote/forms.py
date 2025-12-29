from django import forms
from .models import OccurrenceVote


class OccurrenceVoteForm(forms.ModelForm):
    class Meta:
        model = OccurrenceVote
        fields = ['vote']
        widgets = {
            'vote': forms.RadioSelect()
        }