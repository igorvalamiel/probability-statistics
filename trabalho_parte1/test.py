import numpy as np
from random import shuffle
import json

class BetaBinomial:
    def __init__(self, data, a0=1, b0=1):
        self.betabinData = np.array(data)
        n = 1000
        self.alpha_0 = a0
        self.beta_0 = b0

        xt, nt = self.percentToBin(self.betabinData, n)

        print(f"Conversão para dados binomiais:")
        print(f"Pacotes perdidos (sucessos): {xt}")
        print(f"Total de pacotes (tentativas): {nt}")
        loss_percent = xt/nt
        print(f"Taxa de perda observada: {loss_percent} ({loss_percent*100}%)\n")

        self.alpha, self.beta = self.posterior(xt, nt)

        print("Novos valores para as priors:")
        print(f"Alpha = {self.alpha}")
        print(f"Beta = {self.beta}")

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
    
    def posterior(self, x, n):
        a = self.alpha_0 + x
        b = self.beta_0 + (n-x)
        return a, b