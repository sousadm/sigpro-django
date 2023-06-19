from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse

# Create your models here.

cpf_regex = RegexValidator(
    regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
    message="CPF must be in the format XXX.XXX.XXX-XX"
)


class PessoaModel(models.Model):
    nome = models.CharField(max_length=100)
    fone = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    # definição para pessoa física
    # cpf = models.CharField(
    #     max_length=14,
    #     validators=[cpf_regex]
    # )
    # identidade = models.CharField(max_length=20)
    # pai = models.CharField(max_length=100)
    # mae = models.CharField(max_length=100)
    # nascimento = models.DateField()
    # emissao = models.DateField()
    # orgao = models.CharField(max_length=10)
    # idEstrangeiro = models.CharField(max_length=10)
    # nacionalidade = models.CharField(max_length=30)
    # naturalidade = models.CharField(max_length=30)

    # def get_delete_url(self):
    #     return reverse("url_pessoa_delete", kwargs={"pk": self.pk})

