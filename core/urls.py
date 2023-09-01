"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from acesso.views import login, home, logout
from compra.cotacao import cotacaoEdit, cotacaoNew
from compra.cotacao_item import cotacaoItemNew
from compra.cotacao_orcamento import cotacaoOrcamentoNew
from pessoa.Endereco import get_municipios
from pessoa.views import pessoaNew, pessoaEdit, pessoaClienteEdit, pessoaFornecedorEdit, pessoaTransportadorEdit, \
    pessoaVendedorEdit, pessoaList
from produto.categoria import categoriaList, categoriaEdit, categoriaNew, categoriaChoices
from produto.distribuicao import centroDistribuicaoList, centroDistribuicaoEdit, centroDistribuicaoNew, \
    centroDistribuicaoChoices
from produto.precificacao import precificacaoList, precificacaoEdit, precificacaoNew
from produto.produto import produtoEdit, produtoList, produtoNew
from produto.estoque import produtoEstoque, produtoEstoqueDetalhe

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('pessoa/', pessoaList, name='url_pessoa_list'),
    path('pessoa/add', pessoaNew, name='url_pessoa_add'),
    path('pessoa/<int:uuid>', pessoaEdit, name='url_pessoa_edit'),
    path('pessoa/<int:uuid>/cliente', pessoaClienteEdit, name='url_pessoa_cliente'),
    path('pessoa/<int:uuid>/fornecedor', pessoaFornecedorEdit, name='url_pessoa_fornecedor'),
    path('pessoa/<int:uuid>/transportador', pessoaTransportadorEdit, name='url_pessoa_transportador'),
    path('pessoa/<int:uuid>/vendedor', pessoaVendedorEdit, name='url_pessoa_vendedor'),
    path('get_municipios/', get_municipios, name='get_municipios'),

    path('categoria/', categoriaList, name='url_categoria_list'),
    path('categoria/<int:uuid>', categoriaEdit, name='url_categoria_edit'),
    path('categoria/add', categoriaNew, name='url_categoria_add'),
    path('get_categorias/', categoriaChoices, name='get_categorias'),

    path('precificacao/', precificacaoList, name='url_precificacao_list'),
    path('precificacao/<int:uuid>', precificacaoEdit, name='url_precificacao_edit'),
    path('precificacao/add', precificacaoNew, name='url_precificacao_add'),

    path('produto/', produtoList, name='url_produto_list'),
    path('produto/<int:uuid>', produtoEdit, name='url_produto_edit'),
    path('produto/<int:uuid>/estoque', produtoEstoque, name='url_produto_estoque'),
    path('produto/<int:uuid>/estoque-detalhe', produtoEstoqueDetalhe, name='url_produto_estoque_detalhe'),
    path('produto/add', produtoNew, name='url_produto_add'),

    path('distribuicao/', centroDistribuicaoList, name='url_distribuicao_list'),
    path('distribuicao/<int:uuid>', centroDistribuicaoEdit, name='url_distribuicao_edit'),
    path('distribuicao/add', centroDistribuicaoNew, name='url_distribuicao_add'),
    path('get_distribuicoes/', centroDistribuicaoChoices, name='get_distribuicoes'),

    path('cotacao/add', cotacaoNew, name='url_cotacao_add'),
    path('cotacao/<int:uuid>', cotacaoEdit, name='url_cotacao_edit'),

    path('cotacao/<int:uuid>/add-item', cotacaoItemNew, name='url_cotacaoitem_add'),
    path('cotacao/<int:uuid>/add-orcamento', cotacaoOrcamentoNew, name='url_orcamento_add'),

]
