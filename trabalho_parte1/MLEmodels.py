import scipy.stats as stats
import json
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize
from scipy.special import beta

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

class Gamma():
    def __init__(self, data):
        # getting k and theta
        self.gammaData = np.array(data)
        self.k_mle, self.loc_mle, self.theta_mle = stats.gamma.fit(self.gammaData, floc=0)
        print(f"Parâmetros MLE estimados: k = {self.k_mle}, loc = {self.loc_mle} , θ = {self.theta_mle}\n")

    # creating the MLE Gamma graph
    def MLE_Gamma(self, xname, title, graphSize=(12,6)):
        # Defining "borders" -> Gamma is defined fo x > 0
        x_min = max(0, self.gammaData.min()) # We have to make this to ajust the inferior border
        x_max = self.gammaData.max()# We have to make this to ajust the superior border
        x_grid = np.linspace(x_min, x_max, 1000)

        # Creating the PDF
        pdf_gamma = stats.gamma.pdf(x_grid, self.k_mle, self.loc_mle, self.theta_mle)

        #setting the size
        plt.figure(figsize=graphSize)

        #creating the histogram
        plt.hist(self.gammaData, bins=40, density=True, alpha=0.7, color='#00B30E', label='PDF['+xname+']', edgecolor='black', zorder=1)

        #creating the gamma function
        plt.plot(x_grid, pdf_gamma, '#E88300', linewidth=2.5, label=f'Gamma Ajustada (k={self.k_mle:.3f}, θ={self.theta_mle:.3f})', zorder=2)

        #creating the graph
        plt.xlabel(xname, fontsize=12)
        plt.title(title, fontsize=14)
        plt.legend(fontsize=11)
        plt.grid(alpha=0.3, zorder=0)
        plt.tight_layout()
        plt.yscale('log')

        plt.show()
    
    # Creating the QQplot graph
    def QQplot(self, quantiA, quantiB, title, graphSize=(12,6)):
        #getting size
        plt.figure(figsize=graphSize)

        #getting basic data
        TeoricQuant = stats.gamma.ppf(np.linspace(quantiA, quantiB, len(self.gammaData)), self.k_mle, self.loc_mle, self.theta_mle)
        AmostrQuant = np.sort(self.gammaData)

        #creating the graph and the linear
        plt.scatter(TeoricQuant, AmostrQuant, alpha=0.7, color='#00B30E', label="Dados Reais x Ajuste Gamma")
        plt.plot([TeoricQuant.min(), TeoricQuant.max()], [TeoricQuant.min(), TeoricQuant.max()], "#E88300", linewidth=2, label='Linha de Referência (y=x)')

        # plotting the graph
        plt.xlabel('Quantis Teóricos - Gamma Ajustada')
        plt.ylabel('Quantis Amostrais - Dados Reais')
        plt.title(title)
        plt.legend()
        plt.grid(alpha=0.3)
        plt.yscale('log')
        plt.xscale('log')
        plt.show()

        #Calculating the Pearson Correaltion to verify if the model is great
        correlation, _ = stats.pearsonr(TeoricQuant, AmostrQuant)
        pears = correlation**2

        print(f"Coeficiente de Determinação (R²) do QQ plot: {pears}")
        if pears > 0.95:
            print("Bom ajuste.")
        elif pears > 0.90:
            print("Ajuste razoável.")
        else:
            print("Ajuste ruim.")

#GamCli11DT = Gamma(cli11dt)
#GamCli11DT.MLE_Gamma("Download Throughput", "Cliente 11 - Download Throughput - Distribuição Gamma", (10,7))
#GamCli11DT.QQplot(0.01, 0.05, "Cliente 11 - Download Throughput - Distribuição Gamma", (10,7))

#GamSer07DT = Gamma(ser07dt)
#GamSer07DT.MLE_Gamma("Download Throughput", "Servidor 07 - Download Throughput - Distribuição Gamma", (10,7))
#GamSer07DT.QQplot(0.01, 0.05, "Servidor 07 - Download Throughput - Distribuição Gamma", (10,7))

#GamCli11UT = Gamma(cli11ut)
#GamCli11UT.MLE_Gamma("Upload Throughput", "Cliente 11 - Upload Throughput - Distribuição Gamma", (10,7))
#GamCli11UT.QQplot(0.01, 0.05, "Cliente 11 - Upload Throughput - Distribuição Gamma", (10,7))

#GamSer07UT = Gamma(ser07ut)
#GamSer07UT.MLE_Gamma("Upload Throughput", "Servidor 07 - Upload Throughput - Distribuição Gamma", (10,7))
#GamSer07UT.QQplot(0.01, 0.05, "Servidor 07 - Upload Throughput - Distribuição Gamma", (10,7))

# =========================================================================================================================================
# Calculing Normal MLE

class Normal():
    def __init__(self, data):
        # seeting initial data and getting mu & sigma
        self.normalData = np.array(data)
        self.mu_mle = np.mean(self.normalData)
        self.sigma_mle = np.std(self.normalData, ddof=0)
        print(f"Parâmetros MLE: μ = {self.mu_mle}, σ = {self.sigma_mle}")
    
    # creating the MLE Normal Graph
    def MLE_Normal(self, xname, title, graphSize=(12,6)):
        # getting size
        plt.figure(figsize=graphSize)

        # plotting histogram
        plt.hist(self.normalData, bins=40, density=True, alpha=0.7, color='#00B30E', edgecolor='black', label='PDF['+xname+']')

        # platting the Normal line
        x = np.linspace(self.mu_mle - 4*self.sigma_mle, self.mu_mle + 4*self.sigma_mle, 1000)
        pdf_vals = stats.norm.pdf(x, self.mu_mle, self.sigma_mle)
        plt.plot(x, pdf_vals, '#E88300', linewidth=2.5, label=f'Normal(μ={self.mu_mle:.4f}, σ={self.sigma_mle:.4f})')
    
        #finishing the graph
        plt.xlabel(xname, fontsize=12)
        plt.title(title, fontsize=14)
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.show()
    
    # Creating the QQplot Graph
    def QQplot(self, quantiA, quantiB, title, graphSize=(12,6)):

        plt.figure(figsize=graphSize)

        percentis = np.linspace(quantiA, quantiB, len(self.normalData))

        # Quantis teóricos da distribuição Normal ajustada
        TeoricQuant = stats.norm.ppf(percentis, self.mu_mle, self.sigma_mle)
        
        # Quantis amostrais dos dados reais
        AmostrQuant = np.percentile(self.normalData, percentis * 100)

        # QQ-plot
        plt.scatter(TeoricQuant, AmostrQuant, alpha=0.7, color='#00B30E', label="Dados Reais x Ajuste Normal")
        plt.plot([TeoricQuant.min(), TeoricQuant.max()], [TeoricQuant.min(), TeoricQuant.max()], "#E88300", linewidth=2, label='Linha de Referência (y=x)')
        plt.xlabel('Quantis Teóricos - Normal Ajustada')
        plt.ylabel('Quantis Amostrais - Dados Reais')
        plt.title(title)
        plt.legend()
        plt.grid(alpha=0.3)
        plt.show()

        # Correlação de Pearson (para avaliar ajuste)
        correlation, _ = stats.pearsonr(TeoricQuant, AmostrQuant)
        r2 = correlation**2

        print(f"Coeficiente de Determinação (R²) do QQ plot: {r2}")
        if r2 > 0.95:
            print("Bom ajuste.")
        elif r2 > 0.90:
            print("Ajuste razoável.")
        else:
            print("Ajuste ruim.")

#NorCli11RTTD = Normal(cli11rttd)
#NorCli11RTTD.MLE_Normal("RTT Download", "Cliente 11 - RTT Download - Distribuição Normal", (10,7))
#NorCli11RTTD.QQplot(0.95, 0.99, "Cliente 11 - RTT Download - Distribuição Normal", (10,7))

#NorSer07RTTD = Normal(ser07rttd)
#NorSer07RTTD.MLE_Normal("RTT Download", "Servidor 07 - RTT Download - Distribuição Normal", (10,7))
#NorSer07RTTD.QQplot(0.95, 0.99, "Servidor 07 - RTT Download - Distribuição Normal", (10,7))

#NorCli11RTTU = Normal(cli11rttu)
#NorCli11RTTU.MLE_Normal("RTT Upload", "Cliente 11 - RTT Upload - Distribuição Normal", (10,7))
#NorCli11RTTU.QQplot(0.95, 0.99, "Cliente 11 - RTT Upload - Distribuição Normal", (10,7))

#NorSer07RTTU = Normal(ser07rttu)
#NorSer07RTTU.MLE_Normal("RTT Upload", "Servidor 07 - RTT Upload - Distribuição Normal", (10,7))
#NorSer07RTTU.QQplot(0.95, 0.99, "Servidor 07 - RTT Upload - Distribuição Normal", (10,7))

# =========================================================================================================================================
# Calculing Binomial MLE

def MLE_Beta_Corrigido(data, xname, title, graphSize=(12,6)):
    """
    Ajusta uma distribuição Beta aos dados contínuos - VERSÃO CORRIGIDA
    """
    from scipy.stats import beta
    from scipy.optimize import minimize
    import numpy as np
    import matplotlib.pyplot as plt
    
    data = np.array(data)
    
    print(f"Estatísticas dos dados originais:")
    print(f"Mínimo: {np.min(data):.4f}")
    print(f"Máximo: {np.max(data):.4f}")
    print(f"Média: {np.mean(data):.4f}")
    print(f"Variância: {np.var(data):.4f}")
    
    # Normaliza os dados para [0,1] removendo outliers extremos
    data_clean = data[np.isfinite(data)]  # Remove infinitos
    data_clean = data_clean[~np.isnan(data_clean)]  # Remove NaNs
    
    # Usa percentis para evitar influência de outliers
    q01 = np.percentile(data_clean, 1)
    q99 = np.percentile(data_clean, 99)
    data_norm = (data_clean - q01) / (q99 - q01)
    
    # Garante que está dentro de [0,1]
    data_norm = np.clip(data_norm, 0.001, 0.999)
    
    print(f"\nDados normalizados:")
    print(f"Mínimo: {np.min(data_norm):.4f}")
    print(f"Máximo: {np.max(data_norm):.4f}")
    print(f"Média: {np.mean(data_norm):.4f}")
    
    # Função de verossimilhança negativa COM REGULARIZAÇÃO
    def neg_log_lik(params):
        alpha, beta_param = params
        alpha = max(0.1, alpha)  # Mínimo aumentado para evitar α < 1
        beta_param = max(0.1, beta_param)
        
        # Adiciona penalização para evitar valores muito pequenos
        penalty = 0
        if alpha < 0.5:
            penalty += (0.5 - alpha) * 10
        if beta_param < 0.5:
            penalty += (0.5 - beta_param) * 10
            
        try:
            log_lik = np.sum(beta.logpdf(data_norm, alpha, beta_param))
            return -log_lik + penalty
        except:
            return 1e10  # Retorna valor alto se houver erro
    
    # Estimativas iniciais MAIS CONSERVADORAS
    mean_val = np.mean(data_norm)
    var_val = np.var(data_norm)
    
    # Garante variância mínima
    var_val = max(var_val, 0.01)
    
    # Fórmula mais conservadora
    alpha0 = mean_val * ((mean_val * (1 - mean_val)) / var_val - 1)
    beta0 = (1 - mean_val) * ((mean_val * (1 - mean_val)) / var_val - 1)
    
    # Limites mais conservadores
    alpha0 = max(1.0, min(50, alpha0))  # Força α >= 1
    beta0 = max(1.0, min(50, beta0))    # Força β >= 1
    
    print(f"\nEstimativas iniciais: alpha={alpha0:.4f}, beta={beta0:.4f}")
    
    # Múltiplas tentativas de otimização
    best_result = None
    best_value = np.inf
    
    # Tenta diferentes pontos iniciais
    initial_guesses = [
        [alpha0, beta0],
        [2.0, 2.0],
        [mean_val * 10, (1 - mean_val) * 10],
        [5.0, 5.0]
    ]
    
    for guess in initial_guesses:
        try:
            result = minimize(neg_log_lik, guess, 
                             bounds=[(0.5, 100), (0.5, 100)], 
                             method='L-BFGS-B')
            if result.success and result.fun < best_value:
                best_value = result.fun
                best_result = result
        except:
            continue
    
    if best_result is None:
        # Fallback: usa método dos momentos
        alpha_mle = mean_val * ((mean_val * (1 - mean_val)) / var_val - 1)
        beta_mle = (1 - mean_val) * ((mean_val * (1 - mean_val)) / var_val - 1)
        alpha_mle = max(1.0, alpha_mle)
        beta_mle = max(1.0, beta_mle)
    else:
        alpha_mle, beta_mle = best_result.x
        alpha_mle = max(0.5, alpha_mle)
        beta_mle = max(0.5, beta_mle)
    
    # Gráfico
    plt.figure(figsize=graphSize)
    
    # Histograma dos dados
    plt.hist(data_norm, bins=30, density=True, alpha=0.7, 
             color='#1f77b4', label=f'Dados [{xname}]', 
             edgecolor='black')
    
    # PDF da distribuição Beta ajustada
    x_grid = np.linspace(0.001, 0.999, 200)
    pdf_beta = beta.pdf(x_grid, alpha_mle, beta_mle)
    plt.plot(x_grid, pdf_beta, 'r-', linewidth=2, 
             label=f'Beta MLE (α={alpha_mle:.3f}, β={beta_mle:.3f})')
    
    plt.xlabel('Valores Normalizados', fontsize=12)
    plt.ylabel('Densidade de Probabilidade', fontsize=12)
    plt.title(f'{title}\nDados Normalizados: [{q01:.2f}, {q99:.2f}] → [0, 1]', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    # Estatísticas
    p_medio = alpha_mle / (alpha_mle + beta_mle)
    moda = (alpha_mle - 1) / (alpha_mle + beta_mle - 2) if alpha_mle > 1 and beta_mle > 1 else np.nan
    variancia = (alpha_mle * beta_mle) / ((alpha_mle + beta_mle)**2 * (alpha_mle + beta_mle + 1))
    
    print(f"\n=== RESULTADOS FINAIS ===")
    print(f"alpha = {alpha_mle:.4f}")
    print(f"beta = {beta_mle:.4f}")
    print(f"Parâmetro p médio = {p_medio:.4f}")
    print(f"Média dos dados normalizados = {np.mean(data_norm):.4f}")
    
    if not np.isnan(moda):
        print(f"Moda = {moda:.4f}")
    else:
        print("Moda = indefinida (alpha <= 1 ou beta <= 1)")
        
    print(f"Variância teórica = {variancia:.6f}")
    print(f"Variância dos dados = {np.var(data_norm):.6f}")
    
    return alpha_mle, beta_mle, data_norm

# Teste com a versão corrigida
#alpha, beta, dados_norm = MLE_Beta_Corrigido(cli11pl, "Valores", "Ajuste Distribuição Beta - Corrigido", (10,7))
alpha, beta, dados_norm = MLE_Beta_Corrigido(ser07pl, "Valores", "Ajuste Distribuição Beta - Corrigido", (10,7))

#BinCli11PL.MLE_Binomial("Packet Loss", "Cliente 11 - Packet Loss - Distribuição Binomial", (10,7))
