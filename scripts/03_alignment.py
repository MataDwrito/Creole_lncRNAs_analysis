import os
import subprocess

# Directorios relativos
ruta_indices = "../data/reference/indice"        # carpeta con los índices de Bowtie2
base_indices = "genoma_index"                    # nombre base del índice
ruta_lecturas = "../results/trimming_trimmomatic"  # lecturas ya procesadas
ruta_salida = "../results/alineamiento_tophat2"  # carpeta donde se guardarán los resultados
archivo_anotaciones = "../data/reference/DM_1-3_516_R44_potato.v6.1.hc_gene_models.gff3"

# Archivos de lecturas post-trimming
archivos_lecturas = [
    "clon17R3_1_clean.fastq.gz",
    "clon39R3_1_clean.fastq.gz",
    "clon43R3_1_clean.fastq.gz",
    "colombiaR3_1_clean.fastq.gz",
    "florblancaR3_1_clean.fastq.gz"
]

# Crear carpeta de salida general si no existe
os.makedirs(ruta_salida, exist_ok=True)

# Ejecutar Tophat2 para cada archivo
for archivo in archivos_lecturas:
    lecturas_entrada = os.path.join(ruta_lecturas, archivo)
    directorio_salida_muestra = os.path.join(ruta_salida, os.path.splitext(archivo)[0])
    
    # Crear directorio de salida individual
    os.makedirs(directorio_salida_muestra, exist_ok=True)

    # Comando Tophat2
    comando = [
        "tophat2",
        "-o", directorio_salida_muestra,
        "-p", "12",
        "--b2-sensitive",
        "--library-type", "fr-unstranded",
        "-G", archivo_anotaciones,
        os.path.join(ruta_indices, base_indices),
        lecturas_entrada
    ]

    print(f"Ejecutando Tophat2 para {archivo}...")
    subprocess.run(comando, check=True)

print("Alineamientos completados.")
