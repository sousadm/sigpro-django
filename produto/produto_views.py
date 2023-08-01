from django.contrib import messages
from django.shortcuts import render
from core.controle import require_token
from produto.categoria_forms import CategoriaForm, CategoriaListForm
from produto.precificacao_forms import PrecificacaoListForm, PrecificacaoForm
from produto.produto_forms import ProdutoForm, ProdutoListForm


@require_token
def produtoNew(request):
    return produto_render(request, None)

def produtoEdit(request, uuid):
    return produto_render(request, uuid)

@require_token
def produto_render(request, uuid=None):
    template_name = 'produto/produto_edit.html'

    if request.POST.get('btn_salvar'):
        form = ProdutoForm(request.POST, request=request)
        uuid = form.salvar(request, uuid)
        messages.success(request, 'sucesso ao gravar o registro')

    form = ProdutoForm(request=request, uuid=uuid)
    return render(request, template_name, {'form': form})

@require_token
def produtoList(request):
    template_name = 'produto/produto_list.html'
    try:
        form = ProdutoListForm() \
            if request.POST.get('btn_listar') \
            else ProdutoListForm(request.POST)
        page = form.pesquisar(request)

    except Exception as e:
        messages.error(request, e)
    context = {
        'form': form,
        'page': page
    }
    return render(request, template_name, context)


