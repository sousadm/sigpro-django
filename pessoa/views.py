import json

import requests
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from core.controle import require_token, session_get_token, session_get_headers, format_cpf, format_cnpj
from core.settings import URL_API
from pessoa.Endereco import get_lista_unidade_federacao
from pessoa.forms import PessoaForm, ClienteForm, FornecedorForm, TransportadorForm, VendedorForm, PessoaListForm
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


@require_token
def pessoaFornecedorEdit(request, uuid):
    template_name = 'pessoa/fornecedor_edit.html'
    form = FornecedorForm()
    try:

        if request.POST.get('btn_pessoa'):
            return HttpResponseRedirect(reverse('url_pessoa_edit', kwargs={'uuid': uuid}))

        if request.POST.get('btn_salvar'):
            form = FornecedorForm(request.POST)
            form.salvar(request)
            messages.success(request, 'sucesso ao gravar dados')
            return HttpResponseRedirect(reverse('url_pessoa_fornecedor', kwargs={'uuid': uuid}))

        if request.POST.get('btn_ativar'):
            form.ativar(request, request.POST.get('fornecedorId'))
            return HttpResponseRedirect(reverse('url_pessoa_fornecedor', kwargs={'uuid': uuid}))

    except Exception as e:
        messages.error(request, e)

    form.pesquisaPorPessoa(request, uuid)
    return render(request, template_name, {'form': form})


def pessoaTransportadorEdit(request, uuid):
    template_name = 'pessoa/transportador_edit.html'
    form = TransportadorForm()
    try:

        if request.POST.get('btn_pessoa'):
            return HttpResponseRedirect(reverse('url_pessoa_edit', kwargs={'uuid': uuid}))

        if request.POST.get('btn_salvar'):
            form = TransportadorForm(request.POST)
            form.salvar(request)
            messages.success(request, 'sucesso ao gravar dados')
            return HttpResponseRedirect(reverse('url_pessoa_transportador', kwargs={'uuid': uuid}))

        if request.POST.get('btn_ativar'):
            form.ativar(request, request.POST.get('transportadorId'))
            return HttpResponseRedirect(reverse('url_pessoa_transportador', kwargs={'uuid': uuid}))

    except Exception as e:
        messages.error(request, e)

    form.pesquisaPorPessoa(request, uuid)
    return render(request, template_name, {'form': form})


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


@require_token
def pessoaList(request):
    lista = []
    params = {'sort':'nome,asc'}
    template_name = 'pessoa/pessoa_list.html'
    form = PessoaListForm()
    try:

        if request.POST.get('btn_limpar'):
            form = PessoaListForm()

        if request.POST.get('btn_listar'):
            form = PessoaListForm(request.POST)
            params['nome'] = request.POST['nome']

        lista = form.pesquisar(request, params)
    except Exception as e:
        messages.error(request, e)

    context = {
        'form': form,
        'lista': lista,
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


