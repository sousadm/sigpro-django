import requests
from django import forms
from django.contrib import messages
from django.shortcuts import render

from core.controle import session_get_headers, tratar_error, dados_para_json, require_token
from core.paginacao import get_param, get_page
from core.settings import URL_API
from core.tipos import TIPO_SITUACAO

URL_RECURSO = URL_API + 'centro-distribuicao/'

class CentroDistribuicaoForm(forms.Form):
    id = forms.IntegerField(label='ID', required=False)
    descricao = forms.CharField(max_length=100, label='Descrição', widget=forms.DateInput(attrs={'autofocus': 'true', }), initial='')
    ativo = forms.ChoiceField(label='Situação', choices=TIPO_SITUACAO, initial=True)

    def __init__(self, *args, request, uuid=None, **kwargs):
        super(CentroDistribuicaoForm, self).__init__(*args, **kwargs)
        if uuid:
            print(URL_RECURSO + str(uuid))
            response = requests.get(URL_RECURSO + str(uuid), headers=session_get_headers(request))
            if response.status_code == 200:
                self.initial = response.json()
            else:
                raise Exception(tratar_error(response))

    def salvar(self, request, uuid=None):
        data = dados_para_json(self.data)
        headers = session_get_headers(request)
        if uuid:
            response = requests.patch(URL_RECURSO + str(uuid), json=data, headers=headers)
        else:
            response = requests.post(URL_RECURSO, json=data, headers=headers)
        if response.status_code in [200, 201]:
            return response.json()['id']
        else:
            raise Exception(tratar_error(response))


class CentroDistribuicaoListForm(forms.Form):
    descricao = forms.CharField(label='Pesquisa', required=False,
                                widget=forms.TextInput(
                                    attrs={'autofocus': 'autofocus', 'placeholder': 'digite um valor para pesquisa'}))

    def pesquisar(self, request):
        itens_por_pagina = 5
        self.initial = request.POST or request.GET
        params = get_param(self.initial, itens_por_pagina)
        if self.initial.get('descricao'): params['descricao'] = self.initial.get('descricao')
        headers = session_get_headers(request)
        response = requests.get(URL_RECURSO, headers=headers, params=params)
        if response.status_code == 200:
            self.fields['descricao'].initial = self.initial.get('descricao')
            self.initial = dict(response.json())
            return get_page(self.initial, params)


@require_token
def centroDistribuicaoNew(request):
    return centroDistribuicaoRender(request, None)

@require_token
def centroDistribuicaoEdit(request, uuid):
    return centroDistribuicaoRender(request, uuid)


@require_token
def centroDistribuicaoRender(request, uuid=None):
    template_name = 'produto/distribuicao_edit.html'
    try:
        if request.POST.get('btn_salvar'):
            form = CentroDistribuicaoForm(request.POST, request=request)
            uuid = form.salvar(request, uuid)
            messages.success(request, 'sucesso ao gravar dados')
    except Exception as e:
        messages.error(request, e)
    form = CentroDistribuicaoForm(request=request, uuid=uuid)
    return render(request, template_name, {'form': form})

@require_token
def centroDistribuicaoList(request):
    template_name = 'produto/distribuicao_list.html'
    try:
        form = CentroDistribuicaoListForm() \
            if request.POST.get('btn_listar') \
            else CentroDistribuicaoListForm(request.POST)
        page = form.pesquisar(request)

    except Exception as e:
        messages.error(request, e)
    context = {
        'form': form,
        'page': page
    }
    return render(request, template_name, context)


@require_token
def centroDistribuicaoChoices(request):
    lista = []
    response = requests.get(URL_RECURSO, headers=session_get_headers(request))
    if response.status_code == 200:
        for n in response.json()['content']:
            lista.append((n['id'], n['descricao']))
    return lista

