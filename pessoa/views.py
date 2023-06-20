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
    template_name = 'pessoa/pessoa_edit.html'
    try:
        if request.method == "POST":
            form = PessoaForm(request.POST)
            uuid = form.salvar(request)
            return HttpResponseRedirect(reverse('url_pessoa_edit', kwargs={'uuid': uuid}))
            # if form.is_valid():
            #     headers = session_get_headers(request)
            #     response = requests.post(URL_API+'pessoa', json=form.cleaned_data, headers=headers)
            #     if response.status_code == 201:
            #         uuid = response.json()['id']
            #         return HttpResponseRedirect(reverse('url_pessoa_edit', kwargs={'uuid': uuid}))
            #     else:
            #         messages.error(request, response.json()['mensagem'])
            # else:
            #     messages.error(request, form.errors)
        else:
            form = PessoaForm()
    except Exception as e:
        messages.error(request, e)
    return render(request, template_name, {"form": form})



def pessoaEdit(request, uuid):
    template_name = 'pessoa/pessoa_edit.html'
    try:
        headers = session_get_headers(request)
        response = requests.get(URL_API + 'pessoa/' + str(uuid), headers=headers)
        if response.status_code == 200:
            form = PessoaForm(response.json())
            return render(request, template_name, {'form': form})
        else:
            messages.error('registro não localizado')
            return HttpResponseRedirect(reverse('url_pessoa_add'))
    except Exception as e:
        messages.error(request, e)
        return None
        # return HttpResponseRedirect(reverse('url_pessoa_add'))
