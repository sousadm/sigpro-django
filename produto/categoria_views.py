import requests
from django.contrib import messages
from django.shortcuts import render
from core.controle import require_token, session_get_headers
from core.settings import URL_API
from produto.categoria_forms import CategoriaForm, CategoriaListForm

@require_token
def categoriaNew(request):
    return categoria_render(request, None)


def categoriaEdit(request, uuid):
    return categoria_render(request, uuid)


@require_token
def categoria_render(request, uuid=None):
    template_name = 'produto/categoria_edit.html'

    if request.POST.get('btn_salvar'):
        form = CategoriaForm(request.POST, request=request)
        uuid = form.salvar(request, uuid)
        messages.success(request, 'sucesso ao gravar dados')

    form = CategoriaForm(request=request, uuid=uuid)
    return render(request, template_name, {'form': form})


@require_token
def categoriaList(request):
    template_name = 'produto/categoria_list.html'
    try:
        form = CategoriaListForm() \
            if request.POST.get('btn_listar') \
            else CategoriaListForm(request.POST)
        page = form.pesquisar(request)

    except Exception as e:
        messages.error(request, e)
    context = {
        'form': form,
        'page': page
    }
    return render(request, template_name, context)


@require_token
def categoriaChoices(request):
    categorias = []
    response = requests.get(URL_API + 'categoria', headers=session_get_headers(request))
    print(response)
    # if response.status_code == 200:
    #     for n in response.json():
    #         categorias.append((n['id'], n['descricao']))
    return categorias