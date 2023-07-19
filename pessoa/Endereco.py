from django.http import JsonResponse
from sphinx.util import requests

from core.controle import session_get_headers
from core.settings import URL_API


class UnidadeFederacao:
    def __int__(self, uf, descricao):
        self.uf = uf
        self.descricao = descricao


class Municipio:
    def __int__(self, ibge, uf, descricao):
        self.ibge = ibge
        self.uf = uf
        self.descricao = descricao


def get_lista_unidade_federacao(request):
    headers = session_get_headers(request)
    response = requests.get(URL_API + 'municipio/estados', headers=headers)
    data = []
    for n in response.json():
        data.append((n['sigla'], n['descricao']))
    return data


def get_municipios(request, uf):
    response = requests.get(URL_API + 'municipio/estado/' + str(uf), headers=session_get_headers(request))
    if response.status_code == 200:
        return response.json()


def get_municipios(request):
    data = []
    uf = request.GET.get('uf')
    response = requests.get(URL_API + 'municipio/estado/' + str(uf), headers=session_get_headers(request))
    if response.status_code == 200:
        for n in response.json():
            data.append((n['id'], n['descricao']))
    return JsonResponse(dict(data))

    #return JsonResponse(dict(municipios))

