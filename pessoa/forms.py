import requests
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from core.controle import session_get_token, session_get_headers
from core.settings import URL_API
from pessoa.models import PessoaModel
from django import forms

# Create your tests here.


class PessoaForm(forms.ModelForm):
    class Meta:
        model = PessoaModel
        fields = '__all__'
        exclude = ['uuid']
        labels = {
            'nome':'Nome',
            'email':'E-mail',
            'fone': 'Fone',
        }
        widgets = {
            'uuid': forms.TextInput(attrs={'type': 'hidden'}),
        }

    def salvar(self, request):
        if self.is_valid():
            headers = session_get_headers(request)
            response = requests.post(URL_API+'pessoa', json=self.cleaned_data, headers=headers)
            if response.status_code == 201:
                return response.json()['uuid']
            else:
                messages.error(request, response.json()['mensagem'])
        else:
            messages.error(request, self.errors)

    # def __init__(self, *args, **kwargs):
    #     super(PessoaForm, self).__init__(*args, **kwargs)
    #     self.fields['nome'].widget.attrs['autofocus'] = True

