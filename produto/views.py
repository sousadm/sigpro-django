from typing import Dict, Any

from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from core.controle import require_token
from core.model import Paginacao
from produto.forms import CategoriaForm, CategoriaListForm


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
    lista = Paginator
    template_name = 'produto/categoria_list.html'
    form = CategoriaListForm()
    try:

        if request.POST.get('btn_limpar'):
            form = CategoriaListForm()

        if request.POST.get('btn_novo'):
            return HttpResponseRedirect(reverse('url_categoria_add'))

        if request.POST.get('btn_listar'):
            form = CategoriaListForm(request.POST)

        lista = form.pesquisar(request)

    except Exception as e:
        messages.error(request, e)

    context = {
        'form': form,
        'lista':lista
    }
    return render(request, template_name, context)
