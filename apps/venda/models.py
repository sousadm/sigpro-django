from django.db import models

# Create your models here.

TIPO_PAGAMENTO = (
    ('DINHEIRO','Dinheiro'),
    ('DEBITO','Débito'),
    ('CREDITO','Crédito'),
    ('PIX','Pix'),
    ('DEPOSITO','Depósito'),
)

SITUACAO_CADASTRAL = (
    ('ATIVO', 'Ativo'),
    ('INATIVO', 'Inativo')
)
