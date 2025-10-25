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
        plt.plot([TeoricQuant.min(), TeoricQuant.max()],
                [TeoricQuant.min(), TeoricQuant.max()],
                "#E88300", linewidth=2, label='Linha de Referência (y=x)')
        plt.xlabel('Quantis Teóricos - Normal Ajustada')
        plt.ylabel('Quantis Amostrais - Dados Reais')
        plt.title(title)
        plt.legend()
        plt.grid(alpha=0.3)
        plt.show()

        # Correlação de Pearson (para avaliar ajuste)
        correlation, _ = stats.pearsonr(TeoricQuant, AmostrQuant)
        r2 = correlation**2

        print(f"Coeficiente de Determinação (R²) do QQ plot: {r2:.4f}")
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

