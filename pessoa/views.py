import json

import requests
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from core.controle import require_token, session_get_headers
from core.settings import URL_API
from pessoa.Endereco import get_lista_unidade_federacao
from pessoa.forms import PessoaForm, PessoaListForm
from pessoa.models import TIPO_CHOICES


URL_RECURSO = URL_API + 'pessoa/'

@require_token
def pessoaNew(request):
    return pessoa_render(request, None)


def pessoaEdit(request, uuid):
    return pessoa_render(request, uuid)


@require_token
def pessoa_render(request, uuid=None):
    form = PessoaForm(request=request)
    template_name = 'pessoa/pessoa_edit.html'
    tipo_selected = TIPO_CHOICES[0][0]
    municipios = []
    try:

        if request.POST.get('btn_salvar'):
            form = PessoaForm(request.POST, request=request)
            tipo_selected = form.data.get('tipoPessoa')
            uuid = form.salvar(request, uuid)
            messages.success(request, 'sucesso ao gravar dados')
            return HttpResponseRedirect(reverse('url_pessoa_edit', kwargs={'uuid': uuid}))

        if request.POST.get('btn_ativar'):
            form.ativar(request, uuid)
            return HttpResponseRedirect(reverse('url_pessoa_edit', kwargs={'uuid': uuid}))

        form = PessoaForm(request=request, uuid=uuid)        
        municipios = form.municipios(request, form.initial.get('uf'))
        
    except Exception as e:
        messages.error(request, e)

    ufs = get_lista_unidade_federacao(request)
    tipo_selected = form.initial.get('tipoPessoa')
    context = {
        "form": form,
        "tipo_selected": tipo_selected,
        "tipo_definido": tipo_selected != 'INDEFINIDO',
        'ufs': ufs,
        'municipios': municipios
    }
    return render(request, template_name, context)


@require_token
def pessoaList(request):
    params = {'sort':'nome,asc'}
    template_name = 'pessoa/pessoa_list.html'
    form = PessoaListForm()
    try:

        if request.POST.get('btn_limpar'):
            form = PessoaListForm()

        if request.POST.get('btn_listar'):
            form = PessoaListForm(request.POST)
            params['nome'] = request.POST['descricao']

        page = form.pesquisar(request, params)
    except Exception as e:
        messages.error(request, e)

    context = {
        'form': form,
        'page': page
    }
    return render(request, template_name, context)


@require_token
def get_pessoa_documento(request, docto: str):
    try:
        params = {'cpf' if len(docto) < 14 else 'cnpj': docto}
        headers = session_get_headers(request)
        response = requests.get(URL_RECURSO, headers=headers, params=params)
        data = dict(response.json())
        return JsonResponse(data.get('content')[0])
    except Exception as e:
        return JsonResponse({})


@require_token
def get_pessoa_uuid(request, uuid):
    try:
        headers = session_get_headers(request)
        response = requests.get(URL_RECURSO + str(uuid), headers=headers, params={})
        data = dict(response.json())
        # return JsonResponse(data.get('content')[0])
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({})



@require_token
def pessoaPesquisa(request):
    template_name = 'pessoa/pessoa_pesquisa.html'
    params = {'sort':'nome,asc'}
    form = PessoaListForm(request.POST)
    page = form.pesquisar(request, params)
    return render(request, template_name, {'form': form, 'page': page})



