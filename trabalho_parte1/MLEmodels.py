import scipy.stats as stats
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns # Usado para plots mais bonitos

# colecting data
with open("C:/Users/igorv/OneDrive/Área de Trabalho/Universidade/probest/probability-statistics/trabalho_parte1/var_cli11.json", 'r') as f:
    varCli11 = json.load(f)
with open("C:/Users/igorv/OneDrive/Área de Trabalho/Universidade/probest/probability-statistics/trabalho_parte1/var_ser07.json", 'r') as f:
    varSer07 = json.load(f)

cli11dt = varCli11['cli11dt']
cli11rttd = varCli11['cli11rttd']
cli11ut = varCli11['cli11ut']
cli11rttu = varCli11['cli11rttu']
cli11pl = varCli11['cli11pl']

ser07dt = varSer07['ser07dt']
ser07rttd = varSer07['ser07rttd']
ser07ut = varSer07['ser07ut']
ser07rttu = varSer07['ser07rttu']
ser07pl = varSer07['ser07pl']

# function to clean the list (exclude the negative numbers)
def clean(l):
    cleanL = [x for x in l if x >= 0]
    return cleanL

# cleaning the functions
cli11dt = clean(cli11dt)
cli11rttd = clean(cli11rttd)
cli11ut = clean(cli11ut)
cli11rttu = clean(cli11rttu)
cli11pl = clean(cli11pl)

ser07dt = clean(ser07dt)
ser07rttd = clean(ser07rttd)
ser07ut = clean(ser07ut)
ser07rttu = clean(ser07rttu)
ser07pl = clean(ser07pl)

# =========================================================================================================================================
# Calculing Gamma MLE

def MLE_Gamma(data):
    # getting k and theta
    gammaData = np.array(data)
    k_mle, loc_mle, theta_mle = stats.gamma.fit(gammaData)
    print(f"Parâmetros MLE estimados: k = {k_mle:.4f}, θ = {theta_mle:.4f}\n")
    
    #
    df = pd.DataFrame({'gammaData': gammaData})

    # Calcular o valor da PDF da Gamma ajustada PARA CADA PONTO de dado
    df['pdf_ajustada'] = stats.gamma.pdf(
        df['gammaData'],    # O valor 'x'
        a=k_mle,              # O parâmetro 'k' (shape) ajustado
        scale=theta_mle       # O parâmetro 'θ' (scale) ajustado
    )

    # Ordenar os dados (opcional, bom para inspecionar)
    df = df.sort_values(by='gammaData')

    # Exibir os dados "guardados em conjunto"
    print("DataFrame com dados e valores da PDF ajustada:")
    print(df.head())


    # --- 3. Visualizar o Ajuste (Histograma vs PDF) ---

    print("\nGerando gráfico de ajuste (Histograma vs PDF)...")

    # Configurar o plot
    # Criar grid para a PDF
    x_grid = np.linspace(min(gammaData), max(gammaData), 1000)
    pdf_teorica = stats.norm.pdf(x_grid, k_mle, theta_mle)

    # Plotar
    plt.figure(figsize=(10, 6))

    # Histograma dos dados reais
    plt.hist(gammaData, bins=30, density=True, alpha=0.7, 
            color='lightblue', label='Dados Reais', edgecolor='black')

    # PDF do modelo ajustado
    plt.plot(x_grid, pdf_teorica, 'r-', linewidth=2, 
            label=f'PDF Ajustada (μ={k_mle:.2f}, σ={theta_mle:.2f})')

    plt.xlabel('Valor')
    plt.ylabel('Densidade de Probabilidade')
    plt.title('Comparação: Dados Reais vs Modelo Ajustado (MLE)')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.show()

MLE_Gamma(cli11ut)