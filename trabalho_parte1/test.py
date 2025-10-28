import numpy as np
from random import shuffle
import json

class BetaBinomial:
    def __init__(self, data, a0=1, b0=1):
        self.betabinData = np.array(data)
        self.dataSize = len(data)
        n = 1000
        self.alpha_0 = a0
        self.beta_0 = b0
        trainData, testData = self.repart_data(data)

        xt, nt = self.percentToBin(trainData, n)

        print("======= POSTERIOR DATA =======")
        print(f"Conversão para dados binomiais:")
        print(f"Pacotes perdidos (sucessos): {xt}")
        print(f"Total de pacotes (tentativas): {nt}")
        loss_percent = xt/nt
        print(f"Taxa de perda observada: {loss_percent} ({loss_percent*100}%)")

        self.alpha, self.beta = self.posterior(xt, nt)

        print("======= PREDICTIVE POST DATA =======")
        print("Novos valores para as priors:")
        print(f"Alpha = {self.alpha}")
        print(f"Beta = {self.beta}")

        medtrain, vartrain, proptrain = self.estimative(trainData)
        medtest, vartest, proptest = self.estimative(testData)
        print("======= COMPARING DATA =======")
        print(f"Média Referência (dados-teste) = {medtest}")
        print(f"Media Preditiva = {medtrain}")
        self.compareData(medtrain, medtest)
        print(f"Variância Referência (dados-test) = {medtest}")
        print(f"ariância Preditiva = {medtrain}")
        self.compareData(vartrain, vartest)
        print(f"Proporção Referência (dados-teste) = {proptest}")
        print(f"Proporção Preditiva = {proptrain}")
        self.compareData(proptrain, proptest)

    #function to repart the data
    def repart_data(self, data, division=0.7):
        d = data
        shuffle(d)
        n = int(self.dataSize * division)
        return d[:n], d[n:]

    # ajusting data to binomial
    def percentToBin(self, d, n):
        sucess = 0
        trials = 0

        for p in d:
            l = p/100
            losses = int(round(l * n))
            sucess += losses
            trials += n
        
        return sucess, trials
    
    #function to get posterior data
    def posterior(self, x, n):
        a = self.alpha_0 + x
        b = self.beta_0 + (n-x)
        return a, b

    #function to get estimation, variance and proportion
    def estimative(self, d):
        a = self.alpha
        b = self.beta
        n = len(d)

        #med = (n*a)/(a+b)
        #var = (n*a*b*(n+a+b))/(((a+b)**2)*(a+b+1))
        #prop = a/(a+b)

        med = np.mean(d)
        var = np.var(d)
        prop = med/n

        return med, var, prop

    #function to calculate relative discrepance
    def compareData(self, train, test):
        disc = abs(train - test) / test
        print(f"A discrepância relativa entre as variáveis é {disc}")