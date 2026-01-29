class Imovel:
    def __init__(self, tipo):
        self.tipo = tipo.lower()
        self.valor_final = 0.0
    def calcular_valor(self, quartos, garagem, vagas_estudio, tem_criancas):
        total = 0.0
        if self.tipo == 'apartamento':
            total = 700.0
            if quartos == 2: total += 200.0
            if garagem: total += 300.0
            if not tem_criancas: total *= 0.95
        elif self.tipo == 'casa':
            total = 900.0
            if quartos == 2: total += 250.0
            if garagem: total += 300.0
        elif self.tipo == 'estudio':
            total = 1200.0
            if vagas_estudio >= 2:
                total += 250.0
                if vagas_estudio > 2: total += (vagas_estudio - 2) * 60.0
        self.valor_final = total
        return total
