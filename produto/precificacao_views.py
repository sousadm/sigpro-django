import requests
from django.contrib import messages
from django.shortcuts import render
from core.controle import require_token, session_get_headers
from core.settings import URL_API
from produto.categoria_forms import CategoriaForm, CategoriaListForm
from produto.precificacao_forms import PrecificacaoListForm, PrecificacaoForm


@require_token
def precificacaoNew(request):
    return precificacao_render(request, None)

def precificacaoEdit(request, uuid):
    return precificacao_render(request, uuid)


@require_token
def precificacao_render(request, uuid=None):
    template_name = 'produto/precificacao_edit.html'

    if request.POST.get('btn_salvar'):
        form = PrecificacaoForm(request.POST, request=request)
        uuid = form.salvar(request, uuid)
        messages.success(request, 'sucesso ao gravar dados')

    form = PrecificacaoForm(request=request, uuid=uuid)
    return render(request, template_name, {'form': form})

@require_token
def precificacaoList(request):
    template_name = 'produto/precificacao_list.html'
    try:
        form = PrecificacaoListForm() \
            if request.POST.get('btn_listar') \
            else PrecificacaoListForm(request.POST)
        page = form.pesquisar(request)

    except Exception as e:
        messages.error(request, e)
    context = {
        'form': form,
        'page': page
    }
    return render(request, template_name, context)


@require_token
def precificacaoChoices(request):
    lista = []
    response = requests.get(URL_API + 'precificacao', headers=session_get_headers(request))
    if response.status_code == 200:
        for n in response.json()['content']:
            lista.append((n['id'], n['descricao']))
    return lista