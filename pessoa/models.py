from _pydecimal import Decimal

from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse

from core.tipos import TIPO_SITUACAO

# Create your models here.

#PESSOA_FIELDS = ['nome', 'email', 'fone', 'pessoaId']
CLIENTE_FIELDS = ['clienteId', 'situacaoCliente', 'emailFiscal', 'retencaoIss', 'limiteCredito', 'limitePrazo']
TRANSPORTADOR_FIELDS = ['transportadorId', 'situacaoTransportador', 'codigoRNTRC', 'tipoProprietario']
FORNECEDOR_FIELDS = ['fornecedorId', 'situacaoFornecedor']
VENDEDOR_FIELDS = ['vendedorId', 'situacaoVendedor', 'comissao']

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

TIPO_PROPRIETARIO = (
    ("TAC_AGREGADO", "TAC – Agregado"),
    ("TAC_INDEPENDENTE", "TAC – Independente"),
    ("OUTROS", "Outros")
)


class PessoaModel(models.Model):
    # definição para cliente
    clienteId = models.IntegerField(verbose_name='Código')
    situacaoCliente = models.BooleanField(verbose_name='Situação', choices=TIPO_SITUACAO, default=True)
    emailFiscal = models.EmailField(max_length=254, verbose_name='E-mail Fiscal')
    retencaoIss = models.BooleanField(verbose_name='Retenção ISS', choices=TIPO_SIM_NAO, default=False)
    limiteCredito = models.FloatField(verbose_name='Limite de Crédito', default=0)
    limitePrazo = models.FloatField(verbose_name='Limite de Prazo', default=0)
    # definição para Fornecedor
    fornecedorId = models.IntegerField(verbose_name='Código')
    situacaoFornecedor = models.BooleanField(verbose_name='Situação', choices=TIPO_SITUACAO, default=True)
    # definição para Transportador
    transportadorId = models.IntegerField(verbose_name='Código')
    situacaoTransportador = models.BooleanField(verbose_name='Situação', choices=TIPO_SITUACAO, default=True)
    codigoRNTRC = models.CharField(max_length=20, verbose_name='RNTRC')
    tipoProprietario = models.CharField(max_length=20, choices=TIPO_PROPRIETARIO, default='OUTROS', verbose_name='Tipo')
    # DEFINIÇÃO PARA VENDEDOR
    vendedorId = models.IntegerField(verbose_name='Código')
    situacaoVendedor = models.BooleanField(verbose_name='Situação', choices=TIPO_SITUACAO, default=True)
    comissao = models.FloatField(verbose_name='Comissão %', default=0)

    def define_cliente_url(self):
        return reverse("url_define_cliente", kwargs={"pk": self.pk})


