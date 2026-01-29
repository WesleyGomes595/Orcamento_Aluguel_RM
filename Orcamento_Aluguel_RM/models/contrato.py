class Contrato:
    VALOR_CONTRATO_BASE = 2000.0
    def __init__(self, valor=2000.0):
        self.valor = valor
    def calcular_parcela(self, num_parcelas):
        return self.valor / num_parcelas
