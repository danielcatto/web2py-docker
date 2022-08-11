class Vendas:
    prefacio = '''id_cliente, nome_cliente, codigo_produto, quantidade, valor_total, forma_pagamento, status'''
    def __init__(self, id_cliente, nome_cliente, codigo_produto, quantidade, valor_total, forma_pagamento, status):
        self.id_cliente = id_cliente
        self.nome_cliente = nome_cliente
        self.codigo_produto = codigo_produto
        self.quantidade = quantidade
        self.valor_total = valor_total
        self.forma_pagamento = forma_pagamento
        self.status = status

vendas = Vendas(1, 'vini',1, 10, 10, 'cartão', True)
print(vendas.nome_cliente)