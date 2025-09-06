# -*- coding: utf-8 -*-
import os
import subprocess

# Lista de muestras
muestras = ["clon17R3", "clon39R3", "clon43R3", "colombiaR3", "florblancaR3"]

# Directorios relativos
gtf_base_dir = "../results/ensamblaje_transcriptoma"
cuffquant_base_dir = "../results/cuffquant"
cuffnorm_base_dir = "../results/cuffnorm"

# Crear directorios de salida para cada muestra con sufijo "_normalizado"
for muestra in muestras:
    merged_gtf = os.path.join(gtf_base_dir, muestra.lower(), "merged.gtf")
    abundance_file = os.path.join(cuffquant_base_dir, f"{muestra}_abundancia", "abundances.cxb")
    output_dir = os.path.join(cuffnorm_base_dir, f"{muestra}_normalizado")

    # Verificar que los archivos existen
    if not os.path.exists(abundance_file):
        print(f"El archivo .cxb no existe: {abundance_file}. Saltando muestra: {muestra}")
        continue

    if not os.path.exists(merged_gtf):
        print(f"El archivo GTF no existe: {merged_gtf}. Saltando muestra: {muestra}")
        continue

    # Crear directorio de salida si no existe
    os.makedirs(output_dir, exist_ok=True)

    # Comando cuffnorm
    command = [
        "cuffnorm",
        "--output-format", "cuffdiff",
        "--library-type", "fr-unstranded",
        "-p", "12",
        merged_gtf,
        abundance_file,
        "-o", output_dir
    ]

    print(f"Ejecutando cuffnorm para {muestra}...")
    try:
        subprocess.run(command, check=True)
        print(f"Normalización completada con éxito para la muestra: {muestra}")
    except subprocess.CalledProcessError as e:
        print(f"Error en el proceso de cuffnorm para la muestra: {muestra}. Detalles: {e}")
