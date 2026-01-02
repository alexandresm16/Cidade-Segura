from django import forms
from .models import Occurrence
from django.utils import timezone


class OccurrenceForm(forms.ModelForm):
    occurred_at = forms.DateTimeField(
        label='Data e hora da ocorrência',
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                # Limite no front-end também
                'max': timezone.localtime(timezone.now()).strftime('%Y-%m-%dT%H:%M')
            }
        )
    )

    class Meta:
        model = Occurrence
        fields = [
            'crime_type',
            'description',
            'reference',
            'logradouro',
            'bairro',
            'cidade',
            'uf',
            'latitude',
            'longitude',
            'cep',
            'occurred_at',
        ]

        widgets = {
            'crime_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'reference': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
            'logradouro': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'uf': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': 20
            }),
            'cep': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00000-000'
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001'
            }),
        }

        labels = {
            'crime_type': 'Tipo de Denúncia',
            'description': 'Descrição',
            'reference': 'Ponto de referência',
            'logradouro': 'Logradouro',
            'bairro': 'Bairro',
            'cidade': 'Cidade',
            'uf': 'UF',
            'cep': 'CEP',
            'latitude': 'Latitude',
            'longitude': 'Longitude',
        }

    def clean_occurred_at(self):
        data = self.cleaned_data['occurred_at']
        if data > timezone.now():
            raise forms.ValidationError("A data da ocorrência não pode ser no futuro.")
        return data