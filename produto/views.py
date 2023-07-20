from django.shortcuts import render

from core.controle import require_token


# Create your views here.



@require_token
def pessoaList(request):
    data = {}
    lista = []
    template_name = 'produto/categoria_list.html'
    form = PessoaListForm()
    try:

        if request.POST.get('btn_limpar'):
            form = PessoaListForm()

        if request.POST.get('btn_novo'):
            return HttpResponseRedirect(reverse('url_pessoa_add'))

        if request.POST.get('btn_listar'):
            form = PessoaListForm(request.POST)
            data['nome'] = request.POST['nome']

        lista = form.pesquisar(request, data)
    except Exception as e:
        messages.error(request, e)

    context = {
        'form': form,
        'lista': lista,
    }
    return render(request, template_name, context)





