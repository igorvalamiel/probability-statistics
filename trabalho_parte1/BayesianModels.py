import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import json

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
# Calculing Gamma Model

def analise_exploratoria(d):

    dados = np.array(d)
    
    # Estimativas momentâneas para Gamma
    media = dados.mean()
    variancia = dados.var()
    alpha_est = (media ** 2) / variancia
    beta_est = media / variancia
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # Parâmetros da Gamma
    scale_est = 1/beta_est  # Parâmetro de escala
    
    # 1. Histograma dos dados
    n, bins, patches = ax.hist(dados, bins=30, density=True, alpha=0.7, 
                              color='lightblue', edgecolor='black', linewidth=0.5,
                              label='Dados observados')
    
    # 2. Função densidade de probabilidade (PDF) da Gamma
    x = np.linspace(0, dados.max() * 1.2, 1000)
    pdf = stats.gamma(a=alpha_est, scale=scale_est).pdf(x)
    
    ax.plot(x, pdf, 'r-', linewidth=3, label=f'Gamma(α={alpha_est:.3f}, β={beta_est:.3f})')
    ax.fill_between(x, pdf, alpha=0.2, color='red')
    
    # 3. Marcar estatísticas importantes
    media_gamma = alpha_est / beta_est
    moda_gamma = (alpha_est - 1) / beta_est if alpha_est >= 1 else 0
    media_dados = dados.mean()

    
    ax.set_xlabel('Valor')
    ax.set_ylabel('Densidade')
    #ax.set_yscale('log')
    ax.set_title('Ajuste da Distribuição Gamma aos Dados\n' +
                f'Gamma(α={alpha_est:.3f}, β={beta_est:.3f}, θ={scale_est:.3f})')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Estatísticas da distribuição
    print("\n" + "="*60)
    print("ESTATÍSTICAS DA DISTRIBUIÇÃO GAMMA ESTIMADA")
    print("="*60)
    print(f"Parâmetro de forma (α): {alpha_est}")
    print(f"Parâmetro de taxa (β): {beta_est}")
    print(f"Parâmetro de escala (θ = 1/β): {scale_est}")
    print(f"Média teórica (α/β): {media_gamma}")
    print(f"Média dos dados: {media_dados}")
    print(f"Variância teórica (α/β²): {alpha_est/(beta_est**2)}")
    print(f"Variância dos dados: {dados.var()}")
    print(f"Desvio padrão teórico: {np.sqrt(alpha_est/(beta_est**2))}")
    if alpha_est >= 1:
        print(f"Moda teórica ((α-1)/β): {moda_gamma}")
    else:
        print("Moda: 0 (α < 1)")
    print(f"Assimetria teórica: {2/np.sqrt(alpha_est)}")
    print(f"Assimetria dos dados: {stats.skew(dados)}")


# Gerar visualização da função Gamma
#analise_exploratoria(cli11dt)
#analise_exploratoria(ser07dt)
#analise_exploratoria(cli11ut)
analise_exploratoria(ser07ut)
