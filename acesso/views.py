import requests
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from acesso.forms import LoginForm
from core.controle import session_add_token, session_get, session_get_token, session_required, require_token
from core.settings import URL_API


# Create your views here.

def login(request):
    template_name = 'acesso/login.html'
    try:
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                auth_data = {
                    'login': form.cleaned_data.get('username'),
                    'senha': form.cleaned_data.get('password')
                }
                response = requests.post(URL_API, json=auth_data)
                if response.status_code == 200:
                    session_add_token(request, response.json())
                    return HttpResponseRedirect(reverse('home', kwargs={}))
                else:
                    messages.error(request, 'erro ao acessar o sistema')

        else:
            form = LoginForm()

    except Exception as e:
        messages.error(request, e)

    return render(request, template_name, {"form": form})

#decorator
@require_token
def home(request):
    username = session_get(request, 'username')
    template_name = 'acesso/home.html'
    return render(request, template_name, {'username': username})


def logout(request):
    request.session.clear()
    return HttpResponseRedirect(reverse('login', kwargs={}))
