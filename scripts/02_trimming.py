import os
import subprocess

# Directorios relativos
input_dir = "../data"
output_dir = "../results/trimming_trimmomatic"

# Crear directorio general de salida si no existe
os.makedirs(output_dir, exist_ok=True)

# Archivos input y contaminantes (se asume que los contaminantes están en 'data/')
samples = {
    "Clon17R3": "contaminantes17.fa",
    "Clon39R3": "contaminantes39.fa",
    "Clon43R3": "contaminantes43.fa",
    "ColombiaR3": "contaminantesco.fa",
    "FlorBlancaR3": "contaminantesfl.fa"
}

contaminants_dir = "../data"  # Carpeta donde están los archivos de contaminantes

# Parámetros para Trimmomatic
threads = 12
sliding_window = "SLIDINGWINDOW:4:10"
minlen = "MINLEN:51"

# Comando base para Trimmomatic y FastQC
trimmomatic_cmd = "trimmomatic SE -threads {threads} {input_file} {output_file} ILLUMINACLIP:{adapters}:2:30:10 {sliding_window} {minlen}"
fastqc_cmd = "fastqc {output_file} -o {fastqc_output_dir}"

# Archivo de resultados general
results_file = os.path.join(output_dir, "resultados_trimming.txt")

# Procesar cada muestra
for sample, contaminant_file in samples.items():
    # Crear directorio de salida para cada muestra
    sample_output_dir = os.path.join(output_dir, sample.lower())
    os.makedirs(sample_output_dir, exist_ok=True)

    # Rutas de entrada y salida
    input_file = os.path.join(input_dir, f"{sample}_1.fastq.gz")
    output_file = os.path.join(sample_output_dir, f"{sample.lower()}_1_clean.fastq.gz")

    # Validar existencia del archivo de entrada
    if not os.path.isfile(input_file):
        print(f"El archivo de entrada {input_file} no existe. Saltando muestra {sample}.")
        continue

    # Archivo de contaminantes correspondiente
    adapters = os.path.join(contaminants_dir, contaminant_file)
    fastqc_output_dir_sample = sample_output_dir

    # Comando Trimmomatic
    trimmomatic_command = trimmomatic_cmd.format(
        threads=threads,
        input_file=input_file,
        output_file=output_file,
        adapters=adapters,
        sliding_window=sliding_window,
        minlen=minlen
    )

    # Ejecutar Trimmomatic y guardar salida
    print(f"Ejecutando Trimmomatic para {sample}...")
    with open(results_file, "a") as f:
        f.write(f"Resultados de Trimmomatic para {sample}:\n")
        subprocess.run(trimmomatic_command, shell=True, stdout=f, stderr=f)
        f.write("\n\n")

    # Comando FastQC
    fastqc_command = fastqc_cmd.format(
        output_file=output_file,
        fastqc_output_dir=fastqc_output_dir_sample
    )

    # Ejecutar FastQC
    print(f"Ejecutando FastQC para {sample}...")
    subprocess.run(fastqc_command, shell=True)

print("Proceso completado.")
