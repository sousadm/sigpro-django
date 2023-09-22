import json

from django.http import HttpResponseRedirect
from django.urls import reverse


# DECORATOR
# verifica se o token está na sessão
def require_token(view_func):
    def wrapper(request, *args, **kwargs):
        if session_get_token(request) is None:
            return HttpResponseRedirect(reverse('login', kwargs={}))
        return view_func(request, *args, **kwargs)

    return wrapper


def session_get_headers(request):
    token = session_get_token(request)
    headers = {
        'Authorization': f'Bearer {token}'
    }
    return headers


def session_required(request):
    if session_get_token(request) is None:
        return HttpResponseRedirect(reverse('login', kwargs={}))


# Atribui o token de acesso à sessão
def session_add_token(request, token):
    data = dict(token)
    request.session['username'] = data.get('username')
    request.session['nome'] = data.get('nome')
    request.session['userId'] = data.get('userId')
    request.session['vendedorId'] = data.get('vendedorId')
    request.session['access_token'] = data.get('access_token')


# Obtem o token da sessão
def session_get_token(request):
    return session_get(request, 'access_token')


# Adiciona parâmetro na sessão
def session_add(request, chave, valor):
    request.session[chave] = valor


# Obtem parâmetro gravado na sessão
def session_get(request, chave):
    return request.session.get(chave)


# Remove parâmetro gravado na sessão
def session_delete(request, chave):
    del request.session[chave]


def tratar_error(response):
    try:
        texto = str(response.json())
        data = json.loads(texto.replace("'", '"'))
        mensagem = data.get("mensagem", None)
        message = data.get("message", None)
        return (message or mensagem or data) # + "\n Status:" + data.get('status') + "\n Erro:" + data.get('error')
    except:
        return response.json()


def dados_para_json(self_dados, nones=[]):
    post_data = dict(self_dados)
    post_data.pop('csrfmiddlewaretoken', None)
    post_data.pop('btn_salvar', None)
    for item in nones: post_data.pop(item, None)
    json_data = json.dumps(post_data).replace("[", "").replace("]", "")
    data = json.loads(json_data)
    return data


def format_cpf(cpf):
    cpf = str(cpf)
    return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'


def format_cnpj(cnpj):
    cnpj = str(cnpj)
    return f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}'

