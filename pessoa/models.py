from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse

# Create your models here.

cpf_regex = RegexValidator(
    regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
    message="CPF must be in the format XXX.XXX.XXX-XX"
)

cnpj_regex = RegexValidator(
    regex=r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$',
    message="CNPJ deve estar no formato XX.XXX.XXX/XXXX-XX"
)

TIPO_CHOICES =(
    ("INDEFINIDO", "Indefinida"),
    ("FISICA", "Física"),
    ("JURIDICA", "Jurídica"),
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
    (False, "sim"),
    (True, "não")
)

class PessoaModel(models.Model):
    created_dt = models.DateTimeField()
    updated_dt = models.DateTimeField()
    uuid = models.CharField(max_length=254, verbose_name='Código')
    tipoPessoa = models.CharField(max_length=20, choices=TIPO_CHOICES, default='INDEFINIDO', verbose_name='Tipo')
    nome = models.CharField(max_length=100, verbose_name='Nome') #, help_text='nome completo'
    fone = models.CharField(max_length=20, verbose_name='Fone') #, help_text='número do telefone para contato'
    email = models.EmailField(max_length=254, verbose_name='E-mail') #, help_text='e-mail para contato'
    # definição para pessoa física
    cpf = models.CharField(max_length=14, validators=[cpf_regex], verbose_name='CPF') #, help_text='número do cpf'
    identidade = models.CharField(max_length=20, verbose_name='Identidade') #, help_text='número do RG ou identidade de classe'
    pai = models.CharField(max_length=100, verbose_name='Pai') #, help_text='nome completo do pai'
    mae = models.CharField(max_length=100, verbose_name='Nome da Mãe') #, help_text='nome completo da mãe'
    nascimento = models.DateField(verbose_name='Nascimento') #, help_text='data de nascimento'
    emissao = models.DateField(verbose_name='Emissão') #, help_text='data de emissão'
    orgao = models.CharField(max_length=10, verbose_name='Órgão') #, help_text='órgão emissor'
    idEstrangeiro = models.CharField(max_length=10, verbose_name='Id.Estrangeiro') #, help_text='identidade quando estrangeiro'
    nacionalidade = models.CharField(max_length=30, verbose_name='Nacionalidade') #, help_text='país de origem'
    naturalidade = models.CharField(max_length=30, verbose_name='Naturalidade') #, help_text='cidade ou estado de origem'
    # definição para pessoa jurídica
    cnpj = models.CharField(max_length=18, validators=[cnpj_regex], verbose_name='CNPJ')
    fantasia = models.CharField(max_length=100, verbose_name='Nome de Fantasia')
    IE = models.CharField(max_length=20, verbose_name='Insc.Estadual')
    cnae = models.CharField(max_length=20, verbose_name='CNAE')
    fundacao = models.DateField(verbose_name='Data Fundação')
    incentivoCultural = models.BooleanField(verbose_name='Incentivo Cult.', choices=TIPO_SIM_NAO)
    regime = models.CharField(max_length=32, choices=REGIME_TRIBUTARIO_CHOICES, default=REGIME_TRIBUTARIO_CHOICES[0][0], verbose_name='Reg.Tributário')
    tipoIE = models.CharField(max_length=48, choices=TIPO_CONTRIBUINTE_CHOICES, default=TIPO_CONTRIBUINTE_CHOICES[0][0], verbose_name='Contribuinte')
    # def get_delete_url(self):
    #     return reverse("url_pessoa_delete", kwargs={"pk": self.pk})

