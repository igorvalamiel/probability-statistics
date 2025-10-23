import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# =================== Creating Table Client 07 ===================
# data
Cli11mean = [5.046348e+08, 1.288279e-02, 2.673941e+08, 1.522288e-02, 1.197161e+00]
Cli11median = [6.906440e+08, 1.296300e-02, 3.829509e+08, 1.549400e-02, 5.409766e-01]
Cli11var = [8.322927e+16, 3.897524e-05, 2.726939e+16, 8.347817e-05, 3.785838e+00]
Cli11sd = [2.884948e+08, 6.243015e-03, 1.651344e+08, 9.136639e-03, 1.945723e+00]
Cli11q1 = [7.966507e+07, 0, 1.261511e+07, 0, 0]
Cli11q5 = [1.375673e+08, 0, 6.340967e+07, 0, 0]
Cli11q95 = [0, 1.604520e-02, 0, 1.848660e-02, 5.862084e+00]
Cli11q99 = [0, 2.111484e-02, 0, 3.450892e-02, 9.083913e+00]

# Nomes para as métricas (baseado no que você forneceu)
metric_names = [
    'Download Throughput (bps)',
    'RTT Download (sec)', 
    'Upload Throughput (bps)',
    'RTT Upload (sec)',
    'Packet Loss (%)'
]

# Criar DataFrame
df = pd.DataFrame({
    'Metric': metric_names,
    'Mean': Cli11mean,
    'Median': Cli11median,
    'Variance': Cli11var,
    'Standard Deviation': Cli11sd,
    'Quantis 1%': Cli11q1,
    'Quantis 5%': Cli11q5,
    'Quantis 95%': Cli11q95,
    'Quantis 99%': Cli11q99
})

print("=================== Table Client 11 ===================")
print(df)


# =================== Creating Table Server 07 ===================
# data
Ser07mean = [5.852195e+08, 2.961403e-02, 4.491448e+08, 7.644065e-03, 1.665324e+00]
Ser07median = [7.092044e+08, 9.000000e-03, 5.132518e+08, 5.448000e-03, 8.924578e-02]
Ser07var = [1.079835e+17, 2.880341e-03, 9.297521e+16, 2.620936e-05, 9.697489e+00]
Ser07sd = [3.286084e+08, 5.366881e-02, 3.049184e+08, 5.119508e-03, 3.114079e+00]
Ser07q1 = [3.500471e+07, 0, 2.558636e+07, 0, 0]
Ser07q5 = [8.310088e+07, 0, 4.307091e+07, 0, 0]
Ser07q95 = [0, 1.224712e-01, 0, 1.611750e-02, 8.604312e+00]
Ser07q99 = [0, 2.296715e-01, 0, 1.973980e-02, 1.347944e+01]

# Nomes para as métricas (baseado no que você forneceu)
metric_names = [
    'Download Throughput (bps)',
    'RTT Download (sec)', 
    'Upload Throughput (bps)',
    'RTT Upload (sec)',
    'Packet Loss (%)'
]

# Criar DataFrame
df = pd.DataFrame({
    'Metric': metric_names,
    'Mean': Ser07mean,
    'Median': Ser07median,
    'Variance': Ser07var,
    'Standard Deviation': Ser07sd,
    'Quantis 1%': Ser07q1,
    'Quantis 5%': Ser07q5,
    'Quantis 95%': Ser07q95,
    'Quantis 99%': Ser07q99
})

print("=================== Table Server 07 ===================")
print(df)
