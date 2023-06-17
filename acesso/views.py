from django.contrib import messages
from django.shortcuts import render

from acesso.forms import LoginForm

# Create your views here.

def login(request):
    template_name = 'acesso/login.html'
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            messages.success(request, 'modificado com sucesso')
    else:
        form = LoginForm()
    return render(request, template_name, {"form": form})

