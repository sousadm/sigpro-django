from _pydecimal import Decimal

from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse

from core.tipos import TIPO_SITUACAO

# Create your models here.

cpf_regex = RegexValidator(
    regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
    message="CPF must be in the format XXX.XXX.XXX-XX"
)

cnpj_regex = RegexValidator(
    regex=r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$',
    message="CNPJ deve estar no formato XX.XXX.XXX/XXXX-XX"
)

TIPO_CHOICES = (
    ("INDEFINIDO", "Indefinida"),
    ("FISICA", "Física"),
    ("JURIDICA", "Jurídica"),
)

REGIME_TRIBUTARIO_CHOICES = (
    ("SIMPLES_NACIONAL", "Simples nacional"),
    ("SIMPLES_NACIONAL_EXCESSO_RECEITA", "Simples da receita bruta"),
    ("NORMAL", "Regime normal")
)

TIPO_CONTRIBUINTE_CHOICES = (
    ("CONTRIBUINTE_ICMS", "Contribuinte ICMS"),
    ("CONTRIBUINTE_ISENTO_INSCRICAO_CONTRIBUINTES_ICMS", "Isento de ICMS"),
    ("NAO_CONTRIBUINTE", "Não contribuinte")
)

TIPO_SIM_NAO = (
    (False, "Não"),
    (True, "Sim")
)
