from django.contrib import messages
from django.shortcuts import render

from core.controle import require_token
from produto.estoque_forms import EstoqueForm


@require_token
def precificacao_render(request, uuid=None):
    template_name = 'produto/estoque_edit.html'
    try:
        if request.POST.get('btn_salvar'):
            form = EstoqueForm(request.POST, request=request)
            uuid = form.salvar(request, uuid)
            messages.success(request, 'sucesso ao gravar dados')
    except Exception as e:
        messages.error(request, e)
    form = EstoqueForm(request=request, uuid=uuid)
    return render(request, template_name, {'form': form})
