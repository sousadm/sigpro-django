from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from core.controle import require_token
from produto.forms import CategoriaForm, CategoriaListForm


# Create your views here.



@require_token
def categoriaList(request):
    data = {}
    lista = []
    template_name = 'produto/categoria_list.html'
    form = CategoriaListForm()
    try:

        if request.POST.get('btn_limpar'):
            form = CategoriaListForm()

        if request.POST.get('btn_novo'):
            return HttpResponseRedirect(reverse('url_categoria_add'))

        if request.POST.get('btn_listar'):
            form = CategoriaListForm(request.POST)
            data['nome'] = request.POST['nome']

        lista = form.pesquisar(request, data)
    except Exception as e:
        messages.error(request, e)

    context = {
        'form': form,
        'lista': lista,
    }
    return render(request, template_name, context)
