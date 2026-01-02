from django import forms
from .models import OccurrenceVote


class OccurrenceVoteForm(forms.ModelForm):
    class Meta:
        model = OccurrenceVote
        fields = ['vote']
        widgets = {
            'vote': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vote'].choices = list(self.fields['vote'].choices)