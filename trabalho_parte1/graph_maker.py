import json
import matplotlib.pyplot as plt
import numpy as np

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

#===============================================================================================================================================================
# creating the histogram

# getting the max and the min in the x-line
def get_borders(table1, table2):
    a1, b1 = max(table1), max(table2)
    a2, b2 = min(table1), min(table2)
    return [min(a2,b2), max(a1, b1)]

# function to create the histogram graph
def histogram_double(data1, data2, binNum, title, xline, yline, graphSize=(12,6)):
    # setting the separation
    border = get_borders(data1, data2)
    b = np.linspace(border[0], border[1], binNum)

    # creating the plot
    plt.figure(figsize=graphSize)

    # pltting the first histogram
    plt.hist(
        data1,              # getting the data
        bins=b,             # setting the separation
        alpha=0.6,          # setting the "transparency" to see the other graph
        label="Cliente 11",  # naming the data
        color='green',      # coloring the data
        edgecolor='black'   # coloring the border
    )

    # pltting the first histogram
    plt.hist(
        data2,              # getting the data
        bins=b,             # setting the separation
        alpha=0.6,          # setting the "transparency" to see the other graph
        label="Servidor 07",  # naming the data
        color='orange',      # coloring the data
        edgecolor='black'   # coloring the border
    )
    
    # adjusting the graph (adding titles and captions)
    plt.title(title)
    plt.xlabel(xline)
    plt.ylabel(yline)
    plt.legend(loc='upper right') # captions position
    plt.grid(axis='y', alpha=0.3)

    # showing the histogram
    plt.show()

histogram_double(cli11dt, ser07dt, 40, "Download Throughput (bps)", "bps", "Frequency", (16,8))
#histogram_double(cli11ut, ser07ut, 40, "Upload Throughput (bps)", "bps", "Frequency", (16,8))
#histogram_double(cli11ut, ser07ut, 40, "RTT Download (sec)", "sec", "Frequency", (16,8))
#histogram_double(cli11ut, ser07ut, 40, "RTT Upload (sec)", "sec", "Frequency", (16,8))
#histogram_double(cli11ut, ser07ut, 40, "Packet Loss (%)", "percent", "Frequency", (16,8))