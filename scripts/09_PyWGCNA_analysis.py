import os
import PyWGCNA

# ===========================
# Configuración de rutas
# ===========================
base_dir = os.path.expanduser("~/Creole_lncRNAs_analysis")  # Carpeta raíz del proyecto
expr_file = os.path.join(base_dir, "data/matriz_expresion.csv")
sample_info_file = os.path.join(base_dir, "data/metadatos_muestra.csv")
gene_info_file = os.path.join(base_dir, "data/metadatos_transcritos.csv")
output_dir = os.path.join(base_dir, "results/output_pywgcna")

os.makedirs(output_dir, exist_ok=True)

# ===========================
# Crear objeto PyWGCNA
# ===========================
pywgcna_obj = PyWGCNA.WGCNA(
    name="Solanum_tuberosum_Phureja",
    species="Solanum tuberosum Grupo Phureja",
    geneExpPath=expr_file,
    outputPath=output_dir,
    level="transcript",
    figureType="png",
    save=True
)

# ===========================
# Preprocesamiento y análisis
# ===========================
pywgcna_obj.geneExpr.to_df().head(5)
pywgcna_obj.preprocess()
pywgcna_obj.findModules()

# ===========================
# Actualizar información de muestras
# ===========================
pywgcna_obj.updateSampleInfo(path=sample_info_file, sep=",")

# Colores de metadatos
pywgcna_obj.setMetadataColor("Condition", {
    "MV6-17": "green",
    "MV6-39": "red",
    "MV6-43": "blue",
    "Control": "yellow",
    "Progenitor": "orange"
})

pywgcna_obj.setMetadataColor("Tissue", {"Meristemo": "purple"})

# ===========================
# Actualizar información de genes
# ===========================
pywgcna_obj.updateGeneInfo(path=gene_info_file, sep=",")

# ===========================
# Ejecutar análisis y guardar
# ===========================
pywgcna_obj.analyseWGCNA()
pywgcna_obj.saveWGCNA()

# ===========================
# Visualización de módulos de coexpresión
# ===========================
modules_to_plot = [
    "navy", "tomato.1", "darkgoldenrod.1", "beige.0", "blue.0",
    "ivory.1", "goldenrod.1", "hotpink.0", "azure.0", "purple.0",
    "palegoldenrod.0", "sandybrown", "cornflowerblue.0", "indigo",
    "mintcream.0", "red.1", "cadetblue.0", "lemonchiffon.0",
    "tomato.0", "khaki.0", "royalblue", "burlywood.0", "lightyellow",
    "mediumslateblue", "lightpink.0", "olive.0", "orange.1", "steelblue.0",
    "darkgrey.0", "cyan", "lightsalmon.0", "chocolate", "peru.1",
    "gold.1", "papayawhip.1", "darkorange.0", "mintcream", "lightsteelblue.0"
]

for module in modules_to_plot:
    pywgcna_obj.CoexpressionModulePlot(
        modules=[module],
        numGenes=10,
        numConnections=100,
        minTOM=0
    )
