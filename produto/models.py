from django.db import models
from sphinx.util import requests

from core.controle import session_get_headers
from core.settings import URL_API


class Categoria:
    def __int__(self, id, descricao, tipoProduto):
        self.id = id
        self.tipoProduto = tipoProduto
        self.descricao = descricao

def get_categorias(request):
    response = requests.get(URL_API + 'categoria', headers=session_get_headers(request))
    if response.status_code == 200:
        lista = [Categoria(**data) for data in response.json()]
        return lista
