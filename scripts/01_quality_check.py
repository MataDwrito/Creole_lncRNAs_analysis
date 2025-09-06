import os
import subprocess

# Define directorios relativos
directorio_entrada = "../data"
directorio_salida = "../results/fastqc_reports"

# Lista de archivos .fastq.gz
archivos = [
    'Clon17R3_1.fastq.gz',
    'Clon43R3_1.fastq.gz',
    'Clon39R3_1.fastq.gz',
    'ColombiaR3_1.fastq.gz',
    'FlorBlancaR3_1.fastq.gz'
]

# Crea el directorio de salida si no existe
os.makedirs(directorio_salida, exist_ok=True)

# Ejecuta FastQC para cada archivo
for archivo in archivos:
    archivo_entrada = os.path.join(directorio_entrada, archivo)
    directorio_salida_individual = os.path.join(directorio_salida, archivo.replace('.fastq.gz', ''))
    
    # Crea el directorio específico para el archivo
    os.makedirs(directorio_salida_individual, exist_ok=True)

    # Comando FastQC
    comando = ['fastqc', archivo_entrada, '--outdir', directorio_salida_individual]

    try:
        subprocess.run(comando, check=True)
        print(f'FastQC completado para {archivo}. Resultados en {directorio_salida_individual}.')
    except subprocess.CalledProcessError as e:
        print(f'Error al procesar {archivo}: {e}')
