# Proyecto Google Play - Evaluación 3

## Portada
**Asignatura:** SCY1101 Programación para la Ciencia de Datos  
**Evaluación:** Evaluación Parcial N°3  
**Proyecto:** Google Play Store - Pipeline analítico, modelado y dashboard  
**Entregable principal:** `Evaluacion_3_GooglePlay_Pipeline.ipynb`

## Estructura del proyecto
```text
proyecto-googleplay-ev3/
│
├── data/
│   └── raw/
│       └── googleplaystore.csv
│
├── docs/
│   └── README.md
│
└── Evaluacion_3_GooglePlay_Pipeline.ipynb
```

## Objetivo
Construir un único notebook reproducible que consolide el trabajo desarrollado en la Evaluación 2 y lo extienda para la Evaluación 3, incorporando:
- carga y auditoría del dataset,
- limpieza y transformación de datos,
- análisis exploratorio,
- clustering y modelado supervisado,
- validación de integridad,
- visualizaciones interactivas,
- dashboard en Dash embebido como código ejecutable dentro del mismo notebook.

## Librerías permitidas
- pandas
- numpy
- scikit-learn
- plotly
- matplotlib
- seaborn
- dash

## Guía de inicio rápido
1. Abrir `Evaluacion_3_GooglePlay_Pipeline.ipynb` en Google Colab o Jupyter.
2. Verificar que el archivo `data/raw/googleplaystore.csv` exista en la ruta del proyecto.
3. Ejecutar las celdas en orden, desde la configuración inicial hasta el dashboard.
4. Para levantar el dashboard localmente, ejecutar la última celda y abrir la URL indicada por Dash.

## Contenido del notebook
- Contexto y objetivo del proyecto.
- Carga del dataset original.
- Limpieza, imputación y normalización.
- EDA con gráficos estáticos e interactivos.
- Preparación del dataset para machine learning.
- Clustering con K-Means y PCA para visualización.
- Modelos supervisados base y avanzados.
- Comparación de métricas.
- Auditoría de integridad del dataset.
- Dashboard con Dash para audiencia ejecutiva/técnica.
- Hallazgos, conclusiones y propuestas de mejora.

## Notas de reproducibilidad
- Se utiliza `random_state=42` en divisiones y modelos aleatorios.
- El notebook está diseñado para ser autocontenido dentro de esta estructura mínima.
- No se utiliza Docker ni API REST; el foco está en datos, documentación y dashboard.