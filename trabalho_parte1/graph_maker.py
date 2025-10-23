import matplotlib.pyplot as plt
import numpy as np



# Dados de Exemplo:
# Grupo A: Média mais baixa
grupo_a = np.random.normal(loc=50, scale=10, size=500)
# Grupo B: Média mais alta e mais disperso
grupo_b = np.random.normal(loc=70, scale=15, size=700)

# --- 1. Definir os Bins ---
# É crucial usar os mesmos 'bins' para que as frequências sejam comparáveis
# Usamos o min e max de AMBOS os grupos
todos_dados = np.concatenate([grupo_a, grupo_b])
bins = np.linspace(min(todos_dados), max(todos_dados), 40) # 40 intervalos

# --- 2. Cria o Plot ---
plt.figure(figsize=(12, 6))

# --- 3. Plota o primeiro histograma (Grupo A) ---
plt.hist(
    grupo_a,
    bins=bins,           # Usa os bins definidos
    alpha=0.6,           # Transparência (permite ver o que está por baixo)
    label='Grupo A',
    color='blue',
    edgecolor='black'
)

# --- 4. Plota o segundo histograma (Grupo B) ---
plt.hist(
    grupo_b,
    bins=bins,           # USA OS MESMOS BINS!
    alpha=0.6,
    label='Grupo B',
    color='red',
    edgecolor='black'
)

# --- 5. Adiciona Títulos e Legendas ---
plt.title('Comparação de Distribuições de Frequência')
plt.xlabel('Valor')
plt.ylabel('Frequência Absoluta')
plt.legend(loc='upper right') # Mostra a legenda dos grupos
plt.grid(axis='y', alpha=0.3)

plt.show()