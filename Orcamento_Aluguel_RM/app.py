from flask import Flask, render_template, request, redirect, url_for 
import csv
import os
from datetime import datetime

app = Flask(__name__)

class OrcamentoMaster:
    def __init__(self, form):
        self.tipo = form.get('tipo', 'Apartamento')
        self.quartos = int(form.get('quartos', 1))
        self.vagas = int(form.get('vagas', 0))
        self.garagem = form.get('garagem') == 'true'
        self.criancas = form.get('criancas') == 'true'

    def calcular(self):
        base = {"Apartamento": 700.0, "Casa": 900.0, "Estúdio": 1200.0}
        valor = base.get(self.tipo, 0.0)

        if self.quartos == 2 and self.tipo != "Estúdio":
            valor += 200.0 if self.tipo == "Apartamento" else 250.0

        if self.garagem and self.tipo != "Estúdio":
            valor += 300.0

        if self.tipo == "Estúdio" and self.vagas > 0:
            valor += 250.0 + (max(0, self.vagas - 2) * 60.0)

        if self.tipo == "Apartamento" and self.criancas:
            valor *= 0.95

        return valor

    def gerar_csv(self, fluxo):
        os.makedirs('static/downloads', exist_ok=True)
        nome_arquivo = f'orcamento_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        caminho_completo = os.path.join('static/downloads', nome_arquivo)
        
        try:
            with open(caminho_completo, 'w', newline='', encoding='utf-8-sig') as f:
                w = csv.writer(f, delimiter=';')
                w.writerow(['R.M IMOBILIARIA - RELATORIO TÉCNICO'])
                w.writerow(['MES', 'ALUGUEL BASE', 'TAXA CONTRATO', 'TOTAL MENSAL'])
                for linha in fluxo:
                    w.writerow([f"Mes {linha['m']}", linha['a'], linha['c'], linha['t']])
            return nome_arquivo
        except Exception as e:
            print(f"Erro ao criar CSV: {e}")
            return None

@app.route('/', methods=['GET', 'POST'])
def index():
    dados_resposta = None
    if request.method == 'POST':
        sistema = OrcamentoMaster(request.form)
        valor_base = sistema.calcular()
        fluxo_caixa = []
        parcela_contrato = 2000.0 / 5
        for mes in range(1, 13):
            custo_contrato = parcela_contrato if mes <= 5 else 0.0
            total = valor_base + custo_contrato
            fluxo_caixa.append({
                'm': mes, 
                'a': f"{valor_base:.2f}", 
                'c': f"{custo_contrato:.2f}", 
                't': f"{total:.2f}"
            })
        arquivo_csv = sistema.gerar_csv(fluxo_caixa)
        dados_resposta = {
            'tipo': sistema.tipo,
            'valor': f"{valor_base:.2f}",
            'tabela': fluxo_caixa,
            'csv': arquivo_csv 
        }
    return render_template('index.html', res=dados_resposta)

@app.route('/reset')
def reset():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)