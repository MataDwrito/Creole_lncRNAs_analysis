import pandas as pd
import os

# Crear carpeta de resultados
results_dir = "../results/lncRNA_filtering"
os.makedirs(results_dir, exist_ok=True)

# Archivo de entrada original
isoforms_file = "../results/cuffnorm/isoforms.fpkm_tracking"

# 1️⃣ Filtrar FPKM < 0.001 como 0 y eliminar transcritos con todos FPKM = 0
fpkm_cols = [9, 13, 17, 21, 25]  # Índices 0-based de FPKM (Python)
df = pd.read_csv(isoforms_file, sep='\t')

# Marcar FPKM < 0.001 como 0
df.iloc[:, fpkm_cols] = df.iloc[:, fpkm_cols].applymap(lambda x: 0 if x < 0.001 else x)

# Eliminar transcritos con todos FPKM = 0
df = df[df.iloc[:, fpkm_cols].sum(axis=1) > 0]

filtered_file = os.path.join(results_dir, "filtered_isoforms.fpkm_tracking")
df.to_csv(filtered_file, sep='\t', index=False)
print(f"Paso 1 completado: {filtered_file}")

# 2️⃣ Filtrado por número de exones y valores FPKM
exon_file = "../data/numero_exones_por_transcrito.txt"
exon_df = pd.read_csv(exon_file, sep='\t', header=None, names=["transcript_id", "exon_count"])

df = df.merge(exon_df, left_on="tracking_id", right_on="transcript_id")

def exon_filter(row):
    if row["exon_count"] == 1:
        return any(row.iloc[i] >= 2 for i in fpkm_cols)
    else:
        return any(row.iloc[i] >= 0.5 for i in fpkm_cols)

df = df[df.apply(exon_filter, axis=1)]
df_exon_filtered_file = os.path.join(results_dir, "isoforms_filtrado.fpkm_tracking")
df.to_csv(df_exon_filtered_file, sep='\t', index=False)
print(f"Paso 2 completado: {df_exon_filtered_file}")

# 3️⃣ Filtrar transcritos por longitud > 200 pb
df = df[df["length"] > 200]  # Ajusta la columna que contiene la longitud
df_200pb_file = os.path.join(results_dir, "isoforms_200pb_filtrado.fpkm_tracking")
df.to_csv(df_200pb_file, sep='\t', index=False)
print(f"Paso 3 completado: {df_200pb_file}")

# 4️⃣ Filtrar por longitud ORF < 100
orf_file = "../results/lncRNA_filtering/orf_transcriptos.txt"  # Archivo con transcript_id, ORF_length
orf_df = pd.read_csv(orf_file, sep='\t', header=None, names=["transcript_id", "orf_length"])
df = df.merge(orf_df, on="transcript_id")
df = df[df["orf_length"] < 100]

df_orf_file = os.path.join(results_dir, "isoforms_final_filtrado.fpkm_tracking")
df.to_csv(df_orf_file, sep='\t', index=False)
print(f"Paso 4 completado: {df_orf_file}")

# 5️⃣ Filtrar por CPC <= 0
cpc_file = "../results/lncRNA_filtering/cpc_results.txt"  # Asume columna 6 = CPC score
cpc_df = pd.read_csv(cpc_file, sep='\t')
non_coding_ids = cpc_df[cpc_df.iloc[:, 5] <= 0].iloc[:, 0].tolist()

df = df[df["transcript_id"].isin(non_coding_ids)]
final_non_coding_file = os.path.join(results_dir, "final_non_coding_transcripts.fpkm_tracking")
df.to_csv(final_non_coding_file, sep='\t', index=False)
print(f"Paso 5 completado: {final_non_coding_file}")

# 6️⃣ Extraer IDs de transcritos no codificantes
non_coding_ids_file = os.path.join(results_dir, "non_coding_transcripts_ids.txt")
df["transcript_id"].to_csv(non_coding_ids_file, index=False, header=False)
print(f"IDs de transcritos no codificantes guardados en: {non_coding_ids_file}")
