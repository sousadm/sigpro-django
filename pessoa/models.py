from _pydecimal import Decimal

from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse

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

TIPO_SITUACAO = (
    (False, "Inativo"),
    (True, "Ativo"),
)

TIPO_PROPRIETARIO = (
    ("TAC_AGREGADO", "TAC – Agregado"),
    ("TAC_INDEPENDENTE", "TAC – Independente"),
    ("OUTROS", "Outros")
)


class PessoaModel(models.Model):
    # definição para pessoa física
    cpf = models.CharField(max_length=14, validators=[cpf_regex], verbose_name='CPF')  # , help_text='número do cpf'
    identidade = models.CharField(max_length=20,
                                  verbose_name='Identidade')  # , help_text='número do RG ou identidade de classe'
    pai = models.CharField(max_length=100, verbose_name='Pai')  # , help_text='nome completo do pai'
    mae = models.CharField(max_length=100, verbose_name='Nome da Mãe')  # , help_text='nome completo da mãe'
    nascimento = models.DateField(verbose_name='Nascimento')  # , help_text='data de nascimento'
    emissao = models.DateField(verbose_name='Emissão')  # , help_text='data de emissão'
    orgao = models.CharField(max_length=10, verbose_name='Órgão')  # , help_text='órgão emissor'
    idEstrangeiro = models.CharField(max_length=10,
                                     verbose_name='Id.Estrangeiro')  # , help_text='identidade quando estrangeiro'
    nacionalidade = models.CharField(max_length=30, verbose_name='Nacionalidade')  # , help_text='país de origem'
    naturalidade = models.CharField(max_length=30,
                                    verbose_name='Naturalidade')  # , help_text='cidade ou estado de origem'
    # definição para pessoa jurídica
    cnpj = models.CharField(max_length=18, validators=[cnpj_regex], verbose_name='CNPJ')
    fantasia = models.CharField(max_length=100, verbose_name='Nome de Fantasia')
    IE = models.CharField(max_length=20, verbose_name='Insc.Estadual')
    cnae = models.CharField(max_length=20, verbose_name='CNAE')
    fundacao = models.DateField(verbose_name='Data Fundação')
    incentivoCultural = models.BooleanField(verbose_name='Incentivo Cult.', choices=TIPO_SIM_NAO)
    regime = models.CharField(max_length=32, choices=REGIME_TRIBUTARIO_CHOICES, default=REGIME_TRIBUTARIO_CHOICES[0][0],
                              verbose_name='Reg.Tributário')
    tipoIE = models.CharField(max_length=48, choices=TIPO_CONTRIBUINTE_CHOICES, default=TIPO_CONTRIBUINTE_CHOICES[0][0],
                              verbose_name='Contribuinte')
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


