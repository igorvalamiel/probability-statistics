import matplotlib.pyplot as plt
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

def getDist(data):
    # Supondo que você tenha um array onde o índice é o segundo
    valores = data
    # Criar array de segundos baseado no índice
    segundos = list(range(1, len(valores) + 1))

    # Criar o gráfico de barras
    plt.figure(figsize=(20, 6))
    plt.bar(segundos, valores, color='lightgreen', edgecolor='black')

    # Personalizar o gráfico
    plt.title('Valores Registrados por Segundo', fontsize=14, fontweight='bold')
    plt.xlabel('Segundos', fontsize=12)
    plt.ylabel('Valores', fontsize=12)
    plt.grid(axis='y', alpha=0.3)

    # Ajustar os ticks do eixo x
    plt.xticks(segundos)

    # Mostrar o gráfico
    plt.tight_layout()
    plt.show()

getDist(ser07pl)
