import requests
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from acesso.forms import LoginForm
from core.controle import session_add_token, session_get, require_token
from core.settings import URL_API


# Create your views here.

def login(request):
    template_name = 'acesso/login.html'
    try:
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                response = requests.post(URL_API + 'login', json=form.cleaned_data)
                if response.status_code == 200:
                    session_add_token(request, response.json())
                    # return HttpResponseRedirect(reverse('home'))
                    return HttpResponseRedirect(reverse('url_venda_edit', kwargs={'uuid': 7}))
                    # return HttpResponseRedirect(reverse('url_venda_add'))
                else:
                    messages.error(request, 'erro ao acessar o sistema')
        else:
            form = LoginForm(initial={"login": "gerente"})

    except Exception as e:
        messages.error(request, e)

    return render(request, template_name, {"form": form})


def authenticate_user(self, username, password):
    user = authenticate(username=username, password=password)
    if not user or not user.is_active:
        raise Exception(u"Usuário ou senha inválidos.")
    return user

# decorator
@require_token
def home(request):
    username = session_get(request, 'username')
    template_name = 'acesso/home.html'
    return render(request, template_name, {'username': username})


def logout(request):
    request.session.clear()
    return HttpResponseRedirect(reverse('login', kwargs={}))
