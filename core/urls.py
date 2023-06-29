"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from acesso.views import login, home, logout
from pessoa.views import pessoaNew, pessoaEdit, pessoaClienteEdit

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('pessoa/add', pessoaNew, name='url_pessoa_add'),
    path('pessoa/<int:uuid>', pessoaEdit, name='url_pessoa_edit'),
    path('pessoa/<int:uuid>/cliente', pessoaClienteEdit, name='url_pessoa_cliente'),
]
