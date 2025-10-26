import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from random import shuffle
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
# Calculing Gamma Bayesian Model

class GammaGamma:
    def __init__(self, data, k, initialA, initialB):
        self.gammaData = np.array(data)
        self.dataSize = len(data)
        self.k = k
        trainData, testData = self.repart_data(data)

        self.aP, self.bP = self.posteriori(trainData, initialA, initialB)
        self.ExpectPost = self.aP / self.bP
        self.VarPost = self.aP / (self.bP ** 2)

        print("======= POSTERIOR DATA =======")
        print(f"Posterior Alpha = {self.aP}")
        print(f"Posterior Beta = {self.bP}")
        print(f"Posterior Expected Value = {self.ExpectPost}")
        print(f"Posterior Variance = {self.VarPost}")
        print("======= PREDICTIVE POST DATA =======")
        ExpectPred, VarPred = self.BetaPrime()
        print(f"Média Preditiva = {ExpectPred}")
        print(f"Variância Preditiva = {VarPred}")
        print("======= COMPARING DATA =======")
        self.compareData(ExpectPred, VarPred, testData)
        print('\n')

    def repart_data(self, data, division=0.7):
        d = data
        shuffle(d)
        n = int(self.dataSize * division)
        return d[:n], d[n:]

    def posteriori(self, data, a, b):
        n = len(data)
        sum_data = np.sum(data)
        aP = a + n * self.k
        bP = b + sum_data
        return aP, bP
    
    def BetaPrime(self):
        scale = 1 / self.bP
        print(f"Escala Beta-Prime = {scale}")
        
        if (self.aP > 1):
            Epred = (self.k * self.bP) / (self.aP - 1)
            if (self.aP > 2):
                Vpred = (self.k * (self.k + self.aP - 1) * (self.bP ** 2)) / (((self.aP - 1)**2)*(self.aP - 2))
            else: Vpred = "Não foi possível calcular a Variância, pois an < 2."
        else: Epred = "Não foi possível calcular a Média nem a Variância, pois an < 1."

        return Epred, Vpred
    
    def compareData(self, ev, pv, testD):
        e = np.mean(testD)
        v = np.var(testD)

        print(f"Média Referência (dados-teste) = {e}")
        print(f"Média Preditiva = {ev}")
        discE = abs(ev - e) / e
        print(f"A discrepância relativa entre as médias é {discE}")

        print(f"Variância Referência (dados-test) = {v}")
        print(f"Variância Preditiva = {pv}")
        discV = abs(pv - v) / v
        print(f"A discrepância relativa entre as variâncias é {discV}")


GGCLi11DT = GammaGamma(cli11dt, 2.068843123877114, 0.001, 0.001)
GGSer07DT = GammaGamma(ser07dt, 1.7674622620315197, 0.001, 0.001)
GGCLi11UT = GammaGamma(cli11ut, 1.6047917342609985, 0.001, 0.001)
GGSer07UT = GammaGamma(ser07ut, 1.349178536619483, 0.001, 0.001)

