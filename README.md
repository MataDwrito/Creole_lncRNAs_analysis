
# Pipeline de identificación de ARNlnc en *Solanum tuberosum* (mutantes sólidos)

Este repositorio contiene los scripts para: control de calidad, preprocesamiento,
alineamiento, ensamble de transcritos, identificación de ARNlnc, coexpresión (PyWGCNA)
y enriquecimiento funcional.

## Estructura
- `data/`: Datos de entrada (manejados con Git LFS si superan 100 MB).
- `results/`: Resultados (tablas, figuras, redes).
- `scripts/`: Scripts del pipeline.
- `environment.yml`: Dependencias (Conda).
- `LICENSE`: Licencia.
- `.gitignore`: Archivos ignorados.

## Git LFS
Este repo usa Git LFS para archivos grandes (FASTQ, BAM, SAM, etc.).
Para clonar con datos LFS: git lfs install
git clone https:https://github.com/MataDwrito/Creole_lncRNAs_analysis.git

