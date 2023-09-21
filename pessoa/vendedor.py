import json
from urllib.parse import urlencode
import requests
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms

from core.tipos import NIVEL_NEGOCIACAO, TIPO_SITUACAO
from pessoa.forms import ativar_pessoa_tipo, existe_registro, pesquisa_pessoa, salvar_pessoa_tipo


# VENDEDOR
class VendedorForm(forms.Form):
    pessoaId = forms.IntegerField()
    nome = forms.CharField(max_length=100, label='Nome', disabled=True)
    vendedorId = forms.IntegerField(label='Código', required=False, disabled=True)
    situacaoVendedor = forms.ChoiceField(choices=TIPO_SITUACAO, initial=True)
    nivelNegociacao = forms.ChoiceField(choices=NIVEL_NEGOCIACAO, initial=True)
    comissao = forms.FloatField(label='Percentual de Comissão', initial=0, widget=forms.DateInput(attrs={'autofocus': 'true', }))
    created_dt = forms.DateTimeField(label='Data do cadastro', required=False)

    def existe(self):
        return existe_registro(self, self.initial, 'vendedorId')

    def pesquisaPorPessoa(self, request, uuid):
        self.initial = pesquisa_pessoa(self, request, uuid, 'vendedor')
        print('self.initial', self.initial)

    def json(self):
        post_data = dict(self.data)  # Converter QueryDict para dicionário
        post_data.pop('csrfmiddlewaretoken', None)
        post_data.pop('btn_salvar', None)
        json_data = json.dumps(post_data).replace("[", "").replace("]", "")
        data = json.loads(json_data)
        if data['vendedorId'] == 'None': data['vendedorId'] = None
        return data

    def ativar(self, request, uuid):
        ativar_pessoa_tipo(self, request, 'vendedor', uuid)

    def salvar(self, request):
        data = self.json()
        salvar_pessoa_tipo(self, request, data, 'vendedor')



def pessoaVendedorEdit(request, uuid):
    template_name = 'pessoa/vendedor_edit.html'
    form = VendedorForm()
    try:

        if request.POST.get('btn_pessoa'):
            return HttpResponseRedirect(reverse('url_pessoa_edit', kwargs={'uuid': uuid}))

        if request.POST.get('btn_salvar'):
            form = VendedorForm(request.POST)
            form.salvar(request)
            messages.success(request, 'sucesso ao gravar dados')
            return HttpResponseRedirect(reverse('url_pessoa_vendedor', kwargs={'uuid': uuid}))

        if request.POST.get('btn_ativar'):
            form.ativar(request, request.POST.get('vendedorId'))
            return HttpResponseRedirect(reverse('url_pessoa_vendedor', kwargs={'uuid': uuid}))

    except Exception as e:
        messages.error(request, e)

    form.pesquisaPorPessoa(request, uuid)
    return render(request, template_name, {'form': form})

