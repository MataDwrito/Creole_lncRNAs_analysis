import os
import subprocess

# Directorios relativos
directorio_base = "../results/alineamiento_tophat2"       # carpeta con los BAM de Tophat2
directorio_salida_base = "../results/clout-test"          # carpeta para resultados de Cufflinks
genoma_indice = "../data/reference/DM_1-3_516_R44_potato_genome_assembly.v6.1.fa"

# Carpetas de cada muestra (coincide con los nombres de subcarpetas de Tophat2)
carpetas = [
    "clon17R3_1_clean",
    "clon39R3_1_clean",
    "clon43R3_1_clean",
    "colombiaR3_1_clean",
    "florblancaR3_1_clean"
]

# Crear directorio de salida general si no existe
os.makedirs(directorio_salida_base, exist_ok=True)

# Función para ejecutar Cufflinks
def ejecutar_cufflinks(carpeta):
    bam_entrada = os.path.join(directorio_base, carpeta, "accepted_hits.bam")
    directorio_salida = os.path.join(directorio_salida_base, carpeta)
    
    # Crear directorio de salida individual si no existe
    os.makedirs(directorio_salida, exist_ok=True)

    # Comando Cufflinks
    comando = [
        "cufflinks",
        "-p", "14",
        "-o", directorio_salida,
        "--library-type", "fr-unstranded",
        "-F", "0.05",
        "-u",
        "-b", genoma_indice,
        bam_entrada
    ]
    
    print(f"Ejecutando Cufflinks para {bam_entrada}...")

    # Ejecutar el comando
    resultado = subprocess.run(comando, capture_output=True, text=True)

    # Verificar si el comando se ejecutó correctamente
    if resultado.returncode == 0:
        print(f"Cufflinks completado exitosamente para {bam_entrada}")
    else:
        print(f"Error al ejecutar Cufflinks para {bam_entrada}: {resultado.stderr}")

# Ejecutar Cufflinks para cada carpeta
for carpeta in carpetas:
    ejecutar_cufflinks(carpeta)
