import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.special import beta as beta_func
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

class GammaGamma():
    def __init__(self, data, k, initialA, initialB):
        self.gammaData = np.array(data)
        self.dataSize = len(data)
        self.k = k
        trainData, testData = self.repart_data(data)

        self.aP, self.bP = self.posteriori(trainData, initialA, initialB)
        self.ExpectPost = self.aP / self.bP
        self.VarPost = self.aP / (self.bP ** 2)

        print("========== DADOS DA POSTERIOR ==========")
        print(f"Posterior Alpha = {self.aP}")
        print(f"Posterior Beta = {self.bP}")
        print(f"Posterior Expected Value = {self.ExpectPost}")
        print(f"Posterior Variance = {self.VarPost}\n")

        print(self.BetaPrime(data))

    # function to repart data
    def repart_data(self, d, division=0.7):
        n = int(self.dataSize * division)
        trainD = d[:n]
        testD = d[n:]

        return (trainD, testD)

    # funciton to get posterior
    def posteriori(self, data, a, b):
        n = len(data)
        sum = np.sum(data)
        aP = a + (n*self.k)
        bP = b + sum

        return aP, bP
    
    #funciton to get predictive posterior (Beta Prime Distribution)
    def BetaPrime(self, data):
        #getting scale
        scale = 1/ self.bP

        # getting new Y
        betaPrimSamp = stats.betaprime.rvs(self.aP, self.bP, size=1000)
        predSamp = betaPrimSamp * scale
        Ynew_min = max(0.01, np.min(data) * 0.5)
        Ynew_max = np.max([np.max(data) * 1.5, np.max(predSamp) * 1.1])
        Ynew = np.linspace(Ynew_min, Ynew_max, 1000)
        
        return self.BetaPrimePDF(Ynew, scale)
    
    #defining PDF Beta-Prime function
    def BetaPrimePDF(self, y, s):
        if s == 0:
            return np.zeros_like(y)

        num = (y / s)**(self.aP - 1) * (1 + y / s)**(-self.aP - self.bP)
        pdf = num / (s * beta_func(self.aP, self.bP))
        return np.where(y > 0, pdf, 0)




GGCLi11DT = GammaGamma(cli11dt, 2.068843123877114, 1, 1)
