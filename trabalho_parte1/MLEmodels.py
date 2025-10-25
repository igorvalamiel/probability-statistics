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

GamCli11DT = Gamma(cli11dt)
GamCli11DT.MLE_Gamma("Download Throughput", "Cliente 11 - Download Throughput - Distribuição Gamma", (14,7))

GamSer07DT = Gamma(ser07dt)
GamSer07DT.MLE_Gamma("Download Throughput", "Servidor 07 - Download Throughput - Distribuição Gamma", (14,7))

GamCli11UT = Gamma(cli11ut)
GamCli11UT.MLE_Gamma("Upload Throughput", "Cliente 11 - Upload Throughput - Distribuição Gamma", (14,7))

GamSer07UT = Gamma(ser07ut)
GamSer07UT.MLE_Gamma("Upload Throughput", "Servidor 07 - Upload Throughput - Distribuição Gamma", (14,7))