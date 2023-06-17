
def session_add_token(request, token):
    request.session['username'] = token['username']
    request.session['userId'] = token['userId']
    request.session['access_token'] = token['access_token']

def session_get_token(request):
    return session_get(request, 'access_token')
def session_add(request, chave, valor):
    request.session[chave] = valor

def session_get(request, chave):
    return request.session.get(chave)

def session_delete(request, chave):
    del request.session[chave]
