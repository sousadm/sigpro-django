import json
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from core.controle import require_token

from core.tipos import TIPO_SITUACAO
from apps.pessoa.forms import ativar_pessoa_tipo, existe_registro, pesquisa_pessoa, salvar_pessoa_tipo


@require_token
def pessoaFornecedorEdit(request, uuid):
    template_name = 'pessoa/fornecedor_edit.html'
    form = FornecedorForm()
    try:

        if request.POST.get('btn_pessoa'):
            return HttpResponseRedirect(reverse('url_pessoa_edit', kwargs={'uuid': uuid}))

        if request.POST.get('btn_salvar'):
            form = FornecedorForm(request.POST)
            form.salvar(request)
            messages.success(request, 'sucesso ao gravar dados')
            return HttpResponseRedirect(reverse('url_pessoa_fornecedor', kwargs={'uuid': uuid}))

        if request.POST.get('btn_ativar'):
            form.ativar(request, request.POST.get('fornecedorId'))
            return HttpResponseRedirect(reverse('url_pessoa_fornecedor', kwargs={'uuid': uuid}))

    except Exception as e:
        messages.error(request, e)

    form.pesquisaPorPessoa(request, uuid)
    return render(request, template_name, {'form': form})


class FornecedorForm(forms.Form):
    pessoaId = forms.IntegerField()
    nome = forms.CharField(max_length=100, label='Nome', disabled=True)    
    fornecedorId = forms.IntegerField(label='Código', required=False, disabled=True)
    situacaoFornecedor = forms.ChoiceField(choices=TIPO_SITUACAO, initial=True)
    # nivelNegociacao = forms.ChoiceField(choices=NIVEL_NEGOCIACAO, initial='SEM_DESCONTO')    
    created_dt = forms.DateTimeField(label='Data do cadastro', required=False)

    def existe(self):
        return existe_registro(self, self.initial, 'fornecedorId')

    def pesquisaPorPessoa(self, request, uuid):
        self.initial = pesquisa_pessoa(self, request, uuid, 'fornecedor')

    def json(self):
        post_data = dict(self.data)  # Converter QueryDict para dicionário
        post_data.pop('csrfmiddlewaretoken', None)
        post_data.pop('btn_salvar', None)
        json_data = json.dumps(post_data).replace("[", "").replace("]", "")
        data = json.loads(json_data)
        if data['fornecedorId'] == 'None': data['fornecedorId'] = None
        return data

    def ativar(self, request, uuid):
        ativar_pessoa_tipo(self, request, 'fornecedor', uuid)

    def salvar(self, request):
        data = self.json()
        salvar_pessoa_tipo(self, request, data, 'fornecedor')
