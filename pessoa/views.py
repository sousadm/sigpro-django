import json

import requests
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from core.controle import require_token, session_get_token, session_get_headers, format_cpf, format_cnpj
from core.settings import URL_API
from pessoa.forms import PessoaForm, ClienteForm
from pessoa.models import PessoaModel, TIPO_CHOICES


@require_token
def pessoaNew(request):
    return pessoa_render(request, None)


def pessoaEdit(request, uuid):
    return pessoa_render(request, uuid)


@require_token
def pessoa_render(request, uuid=None):
    template_name = 'pessoa/pessoa_edit.html'
    tipo_selected = TIPO_CHOICES[0][0]
    try:

        if uuid:

            if request.POST.get('btn_cliente'):
                return HttpResponseRedirect(reverse('url_pessoa_cliente', kwargs={'uuid': uuid}))

            response = requests.get(URL_API + 'pessoa/' + str(uuid), headers=session_get_headers(request))
            if response.status_code == 200:
                form = PessoaForm(response.json())
                if form.data.get('cpf'):
                    form.data['cpf'] = format_cpf(form.data.get('cpf'))
                if form.data.get('cnpj'):
                    form.data['cnpj'] = format_cnpj(form.data.get('cnpj'))
                tipo_selected = form.data.get('tipoPessoa')
            else:
                messages.error(request, 'registro não localizado')
        else:
            dados_iniciais = {
                "nome": "Empresa",
                "fone": "00009999",
                "email": "costa@hot.com"
            }
            form = PessoaForm(initial=dados_iniciais)

        if request.POST.get('btn_novo'):
            return HttpResponseRedirect(reverse('url_pessoa_add'))

        if request.POST.get('btn_salvar'):
            form = PessoaForm(request.POST)
            tipo_selected = form.data.get('tipoPessoa')
            uuid = form.salvar(request, uuid)
            messages.success(request, 'sucesso ao gravar dados')
            return HttpResponseRedirect(reverse('url_pessoa_edit', kwargs={'uuid': uuid}))

        if request.POST.get('btn_ativar'):
            form.ativar(request)
            messages.success(request, 'Situação alterada com sucesso')
            return HttpResponseRedirect(reverse('url_pessoa_edit', kwargs={'uuid': uuid}))

    except Exception as e:
        messages.error(request, e)

    context = {
        "form": form,
        "tipo_selected": tipo_selected,
        "tipo_definido": tipo_selected != 'INDEFINIDO',
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
            form.salvar(request, uuid)
            messages.success(request, 'sucesso ao gravar dados')
            return HttpResponseRedirect(reverse('url_pessoa_cliente', kwargs={'uuid': uuid}))

        if request.POST.get('btn_ativar'):
            form.ativar(request)
            messages.success(request, 'Situação alterada com sucesso')
            return HttpResponseRedirect(reverse('url_pessoa_cliente', kwargs={'uuid': uuid}))

    except Exception as e:
        messages.error(request, e)

    form.pesquisaPorPessoa(request, uuid)
    return render(request, template_name, {'form':form})

