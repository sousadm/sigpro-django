import requests
from django.contrib import messages
from django.shortcuts import render

from acesso.forms import LoginForm
from core.settings import URL_API


# Create your views here.

def login(request):
    template_name = 'acesso/login.html'
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            auth_data = {
                'login': form.cleaned_data.get('username'),
                'senha': form.cleaned_data.get('password')
            }
            response = requests.post(URL_API, json=auth_data)
            # messages.success(request, response.status_code)
            if response.status_code == 200:
                messages.success(request, response.text)
                messages.success(request, response.json())
            else:
                messages.success(request, 'erro')

    else:
        form = LoginForm()
    return render(request, template_name, {"form": form})

