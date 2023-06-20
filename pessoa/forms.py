import requests
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from core.controle import session_get_token, session_get_headers, tratar_error
from core.settings import URL_API
from pessoa.models import PessoaModel
from django import forms

# Create your tests here.


class PessoaForm(forms.ModelForm):
    class Meta:
        model = PessoaModel
        fields = '__all__'
        # exclude = ['uuid']
        labels = {
            'uuid':'Código',
            'nome':'Nome',
            'email':'E-mail',
            'fone': 'Fone',
        }


    def salvar(self, request, uuid=None):
        if self.is_valid():
            headers = session_get_headers(request)
            if uuid:
                response = requests.patch(URL_API + 'pessoa/'+str(uuid), json=self.cleaned_data, headers=headers)
            else:
                response = requests.post(URL_API+'pessoa', json=self.cleaned_data, headers=headers)
            if response.status_code in [200,201]:
                return response.json()['uuid']
            else:
                raise Exception(tratar_error(response))
        else:
            raise ValueError(self.errors)

    def __init__(self, *args, **kwargs):
        super(PessoaForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs['autofocus'] = True
        self.fields['uuid'].widget.attrs['disabled'] = 'disabled'
        self.fields['uuid'].required = False



