
def variaveis_globais(request):
    usuario = request.session.get('username')
    return {
        'username': usuario,
        # Outras variáveis
    }
