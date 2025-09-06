# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Carpeta de resultados
results_dir = "../results/differential_expression"
os.makedirs(results_dir, exist_ok=True)

# Ruta del archivo isoform_exp.diff
diff_file = os.path.join(results_dir, "isoform_exp.diff")  # asumiendo que se genera en results/

# Verificar que el archivo existe
if not os.path.exists(diff_file):
    raise FileNotFoundError(f"No se encontró el archivo {diff_file}")

# Cargar el archivo como DataFrame
df = pd.read_csv(diff_file, sep='\t')

# Vista rápida de las primeras filas
print("Primeras filas del archivo original:")
print(df.head())

# Filtrar transcritos significativamente expresados (q-value < 0.05 y significativos)
df_sig = df[(df['q_value'] < 0.05) & (df['significant'] == 'yes')]
print(f"Transcritos diferencialmente expresados: {df_sig.shape[0]}")

# Crear Volcano Plot
df['-log10(q)'] = -np.log10(df['q_value'])

plt.figure(figsize=(10, 6))
plt.scatter(df['log2(fold_change)'], df['-log10(q)'],
            c=(df['significant'] == 'yes').map({True: 'red', False: 'gray'}),
            alpha=0.5)

# Líneas de referencia
plt.axhline(-np.log10(0.05), color='blue', linestyle='--', label='q=0.05')
plt.axvline(1, color='green', linestyle='--', label='Fold Change = ±2')
plt.axvline(-1, color='green', linestyle='--')

plt.title('Volcano Plot de transcritos')
plt.xlabel('log2(Fold Change)')
plt.ylabel('-log10(q-value)')
plt.legend()
plt.grid(True)

# Guardar el gráfico en carpeta results
volcano_path = os.path.join(results_dir, "volcano_plot.png")
plt.savefig(volcano_path, dpi=300)
print(f"Volcano plot guardado en: {volcano_path}")

# Mostrar el gráfico
plt.show()

# Guardar los transcritos significativos en CSV
sig_csv_path = os.path.join(results_dir, "transcritos_significativos.csv")
df_sig.to_csv(sig_csv_path, index=False)
print(f"Archivo de transcritos significativos guardado en: {sig_csv_path}")

# Mostrar las primeras filas del archivo generado
print("Primeras filas de transcritos significativos:")
print(df_sig.head())
