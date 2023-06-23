import json

import requests

from core.controle import session_get_token, session_get_headers, tratar_error
from core.settings import URL_API
from pessoa.models import PessoaModel, TIPO_CHOICES
from django import forms

# Create your tests here.


class PessoaForm(forms.ModelForm):
    class Meta:
        model = PessoaModel
        fields = '__all__'
        exclude = ['created_dt','updated_dt']
        labels = {
            'tipoPessoa':'Tipo de Pessoa',
            'uuid':'Código',
            'nome':'Nome',
            'email':'E-mail',
            'fone': 'Fone',
        }

    def salvar(self, request, uuid=None):
        if self.is_valid():
            headers = session_get_headers(request)
            if uuid:
                response = requests.patch(URL_API + 'pessoa/'+str(uuid), json=self.json(), headers=headers)
            else:
                response = requests.post(URL_API+'pessoa', json=self.json(), headers=headers)
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
        self.fields['cpf'].required = False
        self.fields['identidade'].required = False
        self.fields['pai'].required = False
        self.fields['mae'].required = False
        self.fields['orgao'].required = False

    def json(self):
        post_data = dict(self.data)  # Converter QueryDict para dicionário
        post_data.pop('csrfmiddlewaretoken', None)
        post_data.pop('btn_salvar', None)
        # pessoa fisica
        if self.data.get('tipoPessoa') == TIPO_CHOICES[1][0]:
            cpf = str(self.data.get('cpf'))
            post_data['cpf'] = cpf.replace('.', '').replace('-', '')
        else:
            post_data.pop('cpf', None)
            post_data.pop('identidade', None)
            post_data.pop('orgao', None)
            post_data.pop('pai', None)
            post_data.pop('mae', None)
        json_data = json.dumps(post_data).replace("[", "").replace("]", "")
        return json.loads(json_data)

