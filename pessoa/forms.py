import requests

from core.controle import session_get_token
from core.settings import URL_API
from pessoa.models import PessoaModel
from django import forms

# Create your tests here.


class PessoaForm(forms.ModelForm):
    class Meta:
        model = PessoaModel
        fields = '__all__'

        # labels = {
        #     'nome':'Nome',
        #     'email':'E-mail',
        #     'fone': 'Fone',
        # }
    # def __init__(self, *args, **kwargs):
    #     super(PessoaForm, self).__init__(*args, **kwargs)
    #     self.fields['nome'].widget.attrs['autofocus'] = True

