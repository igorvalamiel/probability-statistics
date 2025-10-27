import numpy as np
from random import shuffle

class NormalNormal:
    def __init__(self, data, mu0, tau0, sigma):
        self.normalData = np.array(data)
        self.dataSize = len(data)
        self.var = sigma**2
        trainData, testData = self.repart_data(data)

        self.mu, self.tau = self.posteriori(trainData, mu0, tau0, self.var)

        print("======= POSTERIOR DATA =======")
        print(f"Posterior Expected Value = {self.mu}")
        print(f"Posterior Variance = {self.tau}")
        print("======= PREDICTIVE POST DATA =======")
        print(f"Média Preditiva = {self.mu}")
        print(f"Variância de erro = {self.var}")
        print(f"Variância de Estimação = {self.tau}")
        self.postVar = self.var + self.tau
        print(f"Variância Preditiva = {self.postVar}")
        print("======= COMPARING DATA =======")
        self.compareData(self.mu, self.postVar, testData)
        print('\n')

    #function to repart the data
    def repart_data(self, data, division=0.7):
        d = data
        shuffle(d)
        n = int(self.dataSize * division)
        return d[:n], d[n:]

    #function to calculate the posteriori
    def posteriori(self, data, mu0, tau0, var):
        n = len(data)
        mean_data = np.mean(data)
        tau_2 = 1 / ((1 / (tau0**2)) + (n / var)) #this tau is squared
        mu = tau_2 * ((mu0 / (tau0**2)) + (n*mean_data / var))
        return mu, tau_2

    #function to compare data
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


