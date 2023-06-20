import json

import requests
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from core.controle import require_token, session_get_token, session_get_headers
from core.settings import URL_API
from pessoa.forms import PessoaForm



@require_token
def pessoaNew(request):
    return pessoa_render(request, None)


def pessoaEdit(request, uuid):
    return pessoa_render(request, uuid)


@require_token
def pessoa_render(request, uuid=None):
    headers = session_get_headers(request)
    template_name = 'pessoa/pessoa_edit.html'
    try:
        if uuid:
            response = requests.get(URL_API + 'pessoa/' + str(uuid), headers=headers)
            if response.status_code == 200:
                form = PessoaForm(response.json())
            else:
                messages.error(request, 'registro não localizado')
        else:
            form = PessoaForm()

        if request.method == "POST":
            form = PessoaForm(request.POST)
            uuid = form.salvar(request, uuid)
            messages.success(request, 'sucesso ao gravar dados')
            return HttpResponseRedirect(reverse('url_pessoa_edit', kwargs={'uuid': uuid}))

    except Exception as e:
        messages.error(request, e)

    return render(request, template_name, {"form": form})