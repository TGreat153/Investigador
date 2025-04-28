from django import forms
from .models import Contratos

class nr_cont_Form(forms.ModelForm):
    class Meta:
        model = Contratos
        fields = '__all__'
