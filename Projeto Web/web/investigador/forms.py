# forms.py
from django import forms

class MeuForm(forms.Form):
    objeto = forms.CharField(
        label='Nome',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    data_inicial = forms.DateField(
        label='Data Inicial',
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    data_final = forms.DateField(
        label='Data Final',
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        data_ini = cleaned_data.get('data_inicial')
        data_fim = cleaned_data.get('data_final')

        if data_ini and data_fim and data_ini > data_fim:
            self.add_error('data_final', 'A data final deve ser maior ou igual à data inicial.')