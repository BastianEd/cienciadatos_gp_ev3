# Google Play Store — Análisis y Pipeline de Datos

**Evaluación Parcial N°3 · SCY1101 Programación para la Ciencia de Datos**  
Duoc UC · 2025

---

## Descripción

Este proyecto realiza un análisis end-to-end del ecosistema de aplicaciones de Google Play Store. A partir del dataset público `googleplaystore.csv`, se construye un pipeline de preprocesamiento, análisis exploratorio, modelado supervisado (clasificación Free/Paid), clustering no supervisado y un dashboard interactivo con Dash.

**Pregunta de trabajo:** ¿qué patrones del ecosistema Google Play permiten describir, segmentar y predecir si una aplicación será gratuita o de pago, y cómo comunicar estos resultados mediante un dashboard profesional?

---

## Estructura del proyecto

```
proyecto-googleplay-ev3/
│
├── data/
│   └── raw/
│       └── googleplaystore.csv              # Dataset original (10.841 registros, 13 columnas)
│
├── README.md                                 # Este archivo
├── requirements.txt                          # Dependencias de Python
├── Evaluacion_3_GooglePlay_Pipeline.ipynb    # Notebook principal (EDA, preprocesamiento, modelado, clustering)
└── dashboard_profesional.py                  # Dashboard interactivo con Dash
```

---

## Dataset

| Campo | Descripción |
|---|---|
| `App` | Nombre de la aplicación |
| `Category` | Categoría en la tienda |
| `Rating` | Calificación promedio (1–5) |
| `Reviews` | Número de reseñas |
| `Size` | Tamaño de la app (MB/KB) |
| `Installs` | Cantidad de instalaciones |
| `Type` | Tipo: Free o Paid |
| `Price` | Precio en USD |
| `Content Rating` | Clasificación de edad |
| `Genres` | Géneros de la app |
| `Last Updated` | Fecha de última actualización |
| `Current Ver` | Versión actual |
| `Android Ver` | Versión mínima de Android requerida |

Fuente: [Kaggle — Google Play Store Apps](https://www.kaggle.com/datasets/lava18/google-play-store-apps)

---

## Requisitos

Python 3.8 o superior. Se recomienda usar un entorno virtual.

### Instalación de dependencias

```bash
pip install -r requirements.txt
```

### Librerías necesarias

| Librería | Propósito |
|---|---|
| `pandas` | Manipulación y análisis de datos |
| `numpy` | Operaciones numéricas y álgebra lineal |
| `matplotlib` | Visualizaciones estáticas |
| `seaborn` | Visualizaciones estadísticas avanzadas |
| `plotly` | Visualizaciones interactivas |
| `scikit-learn` | Machine Learning (preprocesamiento, modelado, clustering) |
| `dash` | Framework web para dashboards interactivos |
| `dash-bootstrap-components` | Componentes Bootstrap para Dash |

**Nota:** El archivo `requirements.txt` incluye todas estas dependencias con versiones mínimas especificadas.

---

## Cómo ejecutar

### Requisitos previos

1. Clonar o descargar el repositorio
2. Asegurar que el archivo `googleplaystore.csv` esté en `data/raw/googleplaystore.csv`
3. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

### A: Ejecutar el Notebook (análisis completo)

```bash
jupyter notebook Evaluacion_3_GooglePlay_Pipeline.ipynb
```

O con JupyterLab:

```bash
jupyter lab Evaluacion_3_GooglePlay_Pipeline.ipynb
```

**Pasos:**
1. Ejecutar todas las celdas en orden con **Run All** o celda por celda
2. El notebook incluye:
   - Exploración y diagnóstico (EDA)
   - Preprocesamiento y limpieza
   - Análisis descriptivo
   - Ingeniería de variables
   - Modelado supervisado (Free vs Paid)
   - Clustering (K-Means + PCA)
   - Validación de integridad

### B: Ejecutar el Dashboard independiente

Si desea ejecutar solo el dashboard profesional sin necesidad de Jupyter:

```bash
python dashboard_profesional.py
```

Luego abrir en el navegador: [http://127.0.0.1:8050](http://127.0.0.1:8050)

**Nota:** El dashboard requiere que el dataset `googleplaystore.csv` esté en `data/raw/googleplaystore.csv`.

---

## Contenido del proyecto

### Notebook: `Evaluacion_3_GooglePlay_Pipeline.ipynb`

| Sección | Descripción |
|---|---|
| **Introducción** | Objetivos, estructura del proyecto y pregunta de trabajo |
| **EDA** | Carga del dataset, auditoría de nulos, duplicados y distribuciones |
| **Preprocesamiento** | Parseo de columnas numéricas, imputación de valores faltantes, detección de outliers por IQR, reglas de consistencia |
| **Análisis descriptivo** | Visualizaciones por categoría, tipo de app, correlaciones de Spearman entre variables numéricas |
| **Ingeniería de variables** | Codificación One-Hot para variables categóricas, split estratificado 80/20 |
| **Modelado supervisado** | Comparación de 3 modelos: Regresión Logística, Random Forest, Gradient Boosting (métricas: Accuracy, F1-macro, AUC-ROC) |
| **Clustering** | Segmentación no supervisada con K-Means (k=4) + proyección PCA, evaluación con Silhouette Score |
| **Validación de integridad** | Auditoría de columnas y validación de reglas de rango sobre el dataset limpio |
| **Informe final** | Hallazgos clave, decisiones técnicas, resultados de negocio y próximos pasos |

### Dashboard: `dashboard_profesional.py`

**Características:**
- **Filtros interactivos:** por categoría, tipo (Free/Paid), rango de rating
- **KPIs en tiempo real:** total de apps, apps de pago, rating promedio
- **Visualizaciones:**
  - Scatter plot: Installs vs Reviews (escala logarítmica)
  - Distribución Free vs Paid
  - Distribución de ratings
  - Top 10 categorías
  - Distribución por Content Rating
  - Análisis de precios
- **Diseño profesional:** paleta Teal Trust (#028090, #00A896, #02C39A), tipografía Cambria/Calibri, responsive layout
- **Tecnologías:** Dash + Plotly + Bootstrap

---

## Flujo del pipeline

```
googleplaystore.csv
        │
        ▼
   Carga y EDA
        │
        ▼
  Preprocesamiento
  (parseo, imputación,
   outliers, consistencia)
        │
        ├──────────────────────────┐
        ▼                          ▼
  Modelado supervisado        Clustering
  (Free vs Paid)              (K-Means + PCA)
        │                          │
        └──────────┬───────────────┘
                   ▼
           Dashboard Dash
         (vista ejecutiva +
           vista técnica)
```

---

## Integrantes

| Nombre | GitHub |
|---|---|
| Bastian | [@BastianEd](https://github.com/BastianEd) |
| Nicolas | [@Excintium](https://github.com/Excintium) |

---

## Rama de desarrollo

- `develop` — rama de trabajo activo
- `main` — versión estable para entrega final

---

## Notas técnicas

- **Autocontención:** El notebook y el dashboard son autocontenidos, sin requerimientos de Docker o servicios externos.
- **Resolución de rutas:** Ambos scripts detectan automáticamente la ubicación del dataset (`data/raw/googleplaystore.csv`) desde la carpeta raíz del proyecto.
- **Reproducibilidad:** Se utiliza `random_state=42` en todos los procesos estocásticos (train_test_split, K-Means, etc.) para garantizar resultados reproducibles.
- **Data leakage:** El preprocesamiento (escalado, imputación) se encapsula en pipelines de scikit-learn para evitar contaminación entre train y test.
- **Desbalance de clases:** Se aplica `class_weight='balanced'` en Random Forest para mitigar el desbalance (mayoría de apps son Free).