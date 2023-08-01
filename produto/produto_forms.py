from django import forms

from produto.models import TIPO_UNIDADE_MEDIDA


class ProdutoForm(forms.Form):
    id = forms.IntegerField(label='ID', required=False)
    descricao = forms.CharField(max_length=100, label='Descrição', widget=forms.DateInput(attrs={'autofocus': 'true', }))
    ncm = forms.CharField(max_length=10, label='NCM')
    cest = forms.CharField(max_length=10, label='CEST')
    unidade = forms.ChoiceField(choices=TIPO_UNIDADE_MEDIDA, initial=TIPO_UNIDADE_MEDIDA[0][0], label='Unidade')
    categoriaId = forms.ChoiceField(choices=(), label='Categoria')
    precificacaoId = forms.ChoiceField(choices=(), label='Precificação')
    precoCompra = forms.DecimalField(initial=0, decimal_places=2, label='Preço de Compra')
    precoVenda = forms.DecimalField(initial=0, decimal_places=2, label='Preço de Venda')
    estoque = forms.FloatField(initial=0, label='Estoque')




