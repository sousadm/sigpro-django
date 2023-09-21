import json
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from core.controle import require_token

from core.tipos import TIPO_SITUACAO
from pessoa.forms import ativar_pessoa_tipo, existe_registro, pesquisa_pessoa, salvar_pessoa_tipo
from pessoa.models import TIPO_SIM_NAO


class ClienteForm(forms.Form):
    pessoaId = forms.IntegerField()
    nome = forms.CharField(max_length=100, label='Nome', disabled=True)    
    clienteId = forms.IntegerField(label='Código', required=False, disabled=True)
    situacaoCliente = forms.ChoiceField(choices=TIPO_SITUACAO, initial=True)
    emailFiscal = forms.EmailField(label='E-mail Fiscal', required=False, widget=forms.DateInput(attrs={'autofocus': 'true', }))
    limiteCredito = forms.FloatField(label='Limite de Crédito', initial=0)
    limitePrazo = forms.FloatField(label='Limite de Prazo', initial=0)
    retencaoIss = forms.ChoiceField(choices=TIPO_SIM_NAO, initial=False, label='Retenção ISS')

    def existe(self):
        return existe_registro(self, self.initial, 'clienteId')

    def pesquisaPorPessoa(self, request, uuid):
        self.initial = pesquisa_pessoa(self, request, uuid, 'cliente')

    def json(self):
        post_data = dict(self.data)  # Converter QueryDict para dicionário
        post_data.pop('csrfmiddlewaretoken', None)
        post_data.pop('btn_salvar', None)
        json_data = json.dumps(post_data).replace("[", "").replace("]", "")
        data = json.loads(json_data)
        if data['clienteId'] == 'None': data['clienteId'] = None
        return data

    def ativar(self, request, uuid):
        ativar_pessoa_tipo(self, request, 'cliente', uuid)

    def salvar(self, request):
        data = self.json()
        salvar_pessoa_tipo(self, request, data, 'cliente')


@require_token
def pessoaClienteEdit(request, uuid):
    template_name = 'pessoa/cliente_edit.html'
    form = ClienteForm()
    try:

        if request.POST.get('btn_pessoa'):
            return HttpResponseRedirect(reverse('url_pessoa_edit', kwargs={'uuid': uuid}))

        if request.POST.get('btn_salvar'):
            form = ClienteForm(request.POST)
            form.salvar(request)
            messages.success(request, 'sucesso ao gravar dados')
            return HttpResponseRedirect(reverse('url_pessoa_cliente', kwargs={'uuid': uuid}))

        if request.POST.get('btn_ativar'):
            form.ativar(request, request.POST.get('clienteId'))
            return HttpResponseRedirect(reverse('url_pessoa_cliente', kwargs={'uuid': uuid}))

    except Exception as e:
        messages.error(request, e)

    form.pesquisaPorPessoa(request, uuid)
    return render(request, template_name, {'form': form})

