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

from apps.acesso.views import login, home, logout
from apps.compra.cotacao import cotacaoEdit, cotacaoImprimir, cotacaoListForm, cotacaoNew
from apps.compra.cotacao_item import cotacaoItemDelete, cotacaoItemEdit, cotacaoItemNew
from apps.compra.cotacao_orcamento import cotacaoOrcamentoDelete, cotacaoOrcamentoEdit, cotacaoOrcamentoNew
from apps.financeiro.caixa import caixaPagamentoNew
from apps.financeiro.centrocusto import centrocustoChoices, centrocustoEdit, centrocustoList, centrocustoNew, centrocustoPesquisa, get_centrocusto_uuid
from apps.financeiro.titulo import tituloEdit, tituloList, tituloNew, tituloPesquisa
from apps.pessoa.Endereco import get_municipios
from apps.pessoa.cliente import pessoaClienteEdit
from apps.pessoa.fornecedor import pessoaFornecedorEdit
from apps.pessoa.transportador import pessoaTransportadorEdit
from apps.pessoa.vendedor import pessoaVendedorEdit
from apps.pessoa.views import get_pessoa_documento, get_pessoa_uuid, pessoaNew, pessoaEdit, pessoaPesquisa, pessoaList
from apps.produto.categoria import categoriaList, categoriaEdit, categoriaNew, categoriaChoices
from apps.produto.distribuicao import centroDistribuicaoList, centroDistribuicaoEdit, centroDistribuicaoNew, \
    centroDistribuicaoChoices
from apps.produto.precificacao import precificacaoList, precificacaoEdit, precificacaoNew
from apps.produto.produto import get_produto, produtoEdit, produtoList, produtoNew, produtoPesquisa
from apps.produto.estoque import produtoEstoque, produtoEstoqueDetalhe
from apps.venda.formapgto import formaPgtoEdit, formaPgtoNew, formapgtoList, get_formapgto
from apps.venda.venda_item import vendaItemDelete, vendaItemEdit, vendaItemNew
from apps.venda.vendas import vendaEdit, vendaImprimir, vendaList, vendaNew

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('pessoa/', pessoaList, name='url_pessoa_list'),
    path('pessoa/pesquisa', pessoaPesquisa, name='url_pessoa_pesquisa'),    
    path('pessoa/add', pessoaNew, name='url_pessoa_add'),
    path('pessoa/<str:docto>/pesquisa-docto', get_pessoa_documento, name='url_pessoa_docto_get'),
    path('pessoa/<int:uuid>/pesquisa', get_pessoa_uuid, name='url_pessoa_get'),
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
    path('produto/pesquisa', produtoPesquisa, name='url_produto_pesquisa'),    
    path('produto/<int:uuid>/pesquisa', get_produto, name='url_produto_get'),
    path('produto/<int:uuid>', produtoEdit, name='url_produto_edit'),
    path('produto/<int:uuid>/detalhe', produtoEdit, name='url_produto_detalhe'),
    path('produto/<int:uuid>/estoque', produtoEstoque, name='url_produto_estoque'),
    path('produto/<int:uuid>/estoque-detalhe', produtoEstoqueDetalhe, name='url_produto_estoque_detalhe'),
    path('produto/add', produtoNew, name='url_produto_add'),

    path('distribuicao/', centroDistribuicaoList, name='url_distribuicao_list'),
    path('distribuicao/<int:uuid>', centroDistribuicaoEdit, name='url_distribuicao_edit'),
    path('distribuicao/add', centroDistribuicaoNew, name='url_distribuicao_add'),
    path('get_distribuicoes/', centroDistribuicaoChoices, name='get_distribuicoes'),

    path('cotacao/', cotacaoListForm, name='url_cotacao_list'),
    path('cotacao/add', cotacaoNew, name='url_cotacao_add'),
    path('cotacao/<int:uuid>', cotacaoEdit, name='url_cotacao_edit'),
    path('cotacao/<int:uuid>/imprimir', cotacaoImprimir, name='url_cotacao_imprimir'),
    path('cotacao/<int:uuid>/add-item', cotacaoItemNew, name='url_cotacaoitem_add'),
    path('cotacao-item/<int:uuid>', cotacaoItemEdit, name='url_cotacaoitem_edit'),
    path('cotacao/<int:uuid>/remove-item/<int:item>', cotacaoItemDelete, name='url_cotacao_remove_item'),
    path('cotacao/<int:uuid>/add-orcamento', cotacaoOrcamentoNew, name='url_orcamento_add'),
    path('cotacao-orcamento/<int:uuid>', cotacaoOrcamentoEdit, name='url_orcamento_edit'),
    path('cotacao/<int:uuid>/remove-orcamento/<int:orcamento>', cotacaoOrcamentoDelete, name='url_cotacao_remove_orcamento'),

    path('formapgto/', formapgtoList, name='url_formapgto_list'),
    path('formapgto/add', formaPgtoNew, name='url_formapgto_add'),
    path('formapgto/<int:uuid>', formaPgtoEdit, name='url_formapgto_edit'),
    path('formapgto/<int:uuid>/pesquisa', get_formapgto, name='url_formapgto_get'),    

    path('venda/', vendaList, name='url_venda_list'),
    path('venda/add', vendaNew, name='url_venda_add'),
    path('venda/<int:uuid>', vendaEdit, name='url_venda_edit'),
    path('venda/<int:uuid>/add-item', vendaItemNew, name='url_vendaitem_add'),
    path('venda-item/<int:uuid>', vendaItemEdit, name='url_vendaitem_edit'),
    path('venda/<int:uuid>/remove-item/<int:item>', vendaItemDelete, name='url_venda_remove_item'),
    path('venda/<int:uuid>/imprimir', vendaImprimir, name='url_venda_imprimir'),

    path('centrocusto/', centrocustoList, name='url_centrocusto_list'),
    path('centrocusto/add', centrocustoNew, name='url_centrocusto_add'),
    path('centrocusto/<int:uuid>', centrocustoEdit, name='url_centrocusto_edit'),
    path('get_centrocustos/', centrocustoChoices, name='get_centrocustos'),
    path('centrocusto/pesquisa', centrocustoPesquisa, name='url_centrocusto_pesquisa'),    
    path('centrocusto/<int:uuid>/pesquisa', get_centrocusto_uuid, name='url_centrocusto_get'),

    path('titulo/', tituloList, name='url_titulo_list'),
    path('titulo/add', tituloNew, name='url_titulo_add'),
    path('titulo/<int:uuid>', tituloEdit, name='url_titulo_edit'),
    path('titulo/pesquisa', tituloPesquisa, name='url_titulo_pesquisa'),    

    path('caixa/pagamento', caixaPagamentoNew, name='url_caixa_pagamento'),

]
