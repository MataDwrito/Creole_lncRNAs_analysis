# -*- coding: utf-8 -*-
import os
import subprocess

# Lista de muestras
muestras = ["clon17R3", "clon39R3", "clon43R3", "colombiaR3", "florblancaR3"]

# Rutas relativas
genome_index = "../data/reference/genoma_index.fa"  # índice del genoma
merged_gtf = "../results/ensamblaje_transcriptoma/merged.gtf"  # GTF maestro
bam_base_dir = "../results/alineamiento_tophat2"  # carpeta con BAMs de Tophat2
output_base_dir = "../results/cuffquant"  # carpeta para resultados de cuffquant

# Verificar que el archivo GTF maestro existe
if not os.path.exists(merged_gtf):
    print(f"El archivo GTF maestro no existe: {merged_gtf}")
else:
    for muestra in muestras:
        # Ruta del BAM de cada muestra
        bam_path = os.path.join(bam_base_dir, f"{muestra}_1_clean", "accepted_hits.bam")
        output_dir = os.path.join(output_base_dir, f"{muestra}_abundancia")

        # Verificar que el archivo BAM existe
        if not os.path.exists(bam_path):
            print(f"El archivo BAM no existe: {bam_path}. Saltando muestra: {muestra}")
            continue

        # Crear el directorio de salida si no existe
        os.makedirs(output_dir, exist_ok=True)

        # Comando cuffquant
        command = [
            "cuffquant",
            "-p", "4",
            "--library-type", "fr-unstranded",
            "--multi-read-correct",
            "--frag-bias-correct", genome_index,
            merged_gtf,
            bam_path,
            "-o", output_dir
        ]

        print(f"Ejecutando cuffquant para {muestra}...")
        try:
            subprocess.run(command, check=True)
            print(f"Proceso completado con éxito para la muestra: {muestra}")
        except subprocess.CalledProcessError as e:
            print(f"Error en el proceso de cuffquant para la muestra: {muestra}. Detalles: {e}")
