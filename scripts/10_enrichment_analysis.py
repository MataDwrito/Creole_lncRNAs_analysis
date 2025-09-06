from gprofiler import GProfiler
import pandas as pd
import os

# ===========================
# Configuración de rutas
# ===========================
base_dir = os.path.expanduser("~/Creole_lncRNAs_analysis")
results_dir = os.path.join(base_dir, "results/gprofiler")
os.makedirs(results_dir, exist_ok=True)

# ===========================
# Lista de genes/transcritos de interés
# ===========================
genes_interes = [
    "gene1", "gene2", "gene3",  # <- reemplaza con tus transcritos o genes
]

# ===========================
# Inicializar GProfiler
# ===========================
gp = GProfiler(return_dataframe=True)

# ===========================
# Ejecutar enriquecimiento funcional
# ===========================
enrichment_results = gp.profile(
    organism='ssc',  # Cambia según tu especie, e.g. 'ssc' para Solanum tuberosum si está disponible
    query=genes_interes,
    sources=['GO:BP', 'GO:MF', 'GO:CC', 'KEGG', 'REAC']
)

# ===========================
# Guardar resultados
# ===========================
output_file = os.path.join(results_dir, "enrichment_results.csv")
enrichment_results.to_csv(output_file, index=False)

print(f"Enriquecimiento funcional guardado en: {output_file}")
