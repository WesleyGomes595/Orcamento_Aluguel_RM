import csv
import os
class Orcamento:
    def __init__(self, imovel):
        self.imovel = imovel
    def gerar_csv(self, filename='orcamento.csv'):
        if not os.path.exists('output'): os.makedirs('output')
        filepath = os.path.join('output', filename)
        with open(filepath, 'w', newline='', encoding='utf-8') as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(['Mes', 'Valor do Aluguel'])
            for mes in range(1, 13):
                writer.writerow([mes, f'R$ {self.imovel.valor_final:.2f}'])
        return filepath
