from django.http import HttpResponseRedirect
from django.urls import reverse


#DECORATOR
#verifica se o token está na sessão
def require_token(view_func):
    def wrapper(request, *args, **kwargs):
        if session_get_token(request) is None:
            return HttpResponseRedirect(reverse('login', kwargs={}))
        return view_func(request, *args, **kwargs)

    return wrapper


def session_required(request):
    if session_get_token(request) is None:
        return HttpResponseRedirect(reverse('login', kwargs={}))


# Atribui o token de acesso à sessão
def session_add_token(request, token):
    request.session['username'] = token['username']
    request.session['userId'] = token['userId']
    request.session['access_token'] = token['access_token']


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
