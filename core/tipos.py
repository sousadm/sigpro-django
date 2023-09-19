

TIPO_SITUACAO = (
    (False, "Inativo"),
    (True, "Ativo"),
)

TIPO_PROPRIETARIO = (
    ("TAC_AGREGADO", "TAC – Agregado"),
    ("TAC_INDEPENDENTE", "TAC – Independente"),
    ("OUTROS", "Outros")
)

NIVEL_NEGOCIACAO = (
    ('SEM_DESCONTO', 'Não pode negociar desconto'),
    ('MARGEM_DE_MERCADO', 'Permitido diferença de preço ref. ao mercado'),
    ('MARGEM_DE_NEGOCIACAO', 'Permitido negociar margem de preço'),
    ('MARGEM_DE_LUCRO', 'Permitido negociar margem de lucro'),
    ('CUSTO_VARIAVEL', 'Permitido negociar margem de custo'),
)

