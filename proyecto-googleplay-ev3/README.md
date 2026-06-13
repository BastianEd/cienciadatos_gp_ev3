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
│       └── googleplaystore.csv       # Dataset original (10.841 registros, 13 columnas)
│
├── docs/
│   └── README.md                     # Este archivo
│
└── Evaluacion_3_GooglePlay_Pipeline.ipynb   # Notebook principal
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

```bash
pip install pandas numpy matplotlib seaborn plotly scikit-learn dash
```

O bien, instalar desde un archivo de dependencias:

```bash
pip install -r requirements.txt
```

`requirements.txt` sugerido:

```
pandas>=1.5
numpy>=1.23
matplotlib>=3.6
seaborn>=0.12
plotly>=5.13
scikit-learn>=1.2
dash>=2.9
```

---

## Cómo ejecutar

### 1. Clonar el repositorio

```bash
git clone https://github.com/BastianEd/cienciadatos_gp_ev3.git
cd cienciadatos_gp_ev3/proyecto-googleplay-ev3
```

### 2. Colocar el dataset

Asegurarse de que el archivo `googleplaystore.csv` esté en:

```
data/raw/googleplaystore.csv
```

### 3. Abrir el notebook

```bash
jupyter notebook Evaluacion_3_GooglePlay_Pipeline.ipynb
```

O con JupyterLab:

```bash
jupyter lab Evaluacion_3_GooglePlay_Pipeline.ipynb
```

Ejecutar todas las celdas en orden con **Run All**.

### 4. Levantar el dashboard

Al final del notebook, descomentar la última línea de la celda del dashboard:

```python
app.run(debug=False, port=8050)
```

Luego abrir en el navegador: [http://127.0.0.1:8050](http://127.0.0.1:8050)

---

## Contenido del notebook

| Sección | Descripción |
|---|---|
| EDA | Carga del dataset, auditoría de nulos, duplicados y distribuciones |
| Preprocesamiento | Parseo de columnas numéricas, imputación, outliers por IQR, reglas de consistencia |
| Análisis descriptivo | Visualizaciones por categoría, tipo y correlaciones de Spearman |
| Ingeniería de variables | Codificación OHE, split estratificado 80/20 |
| Modelado supervisado | Regresión Logística, Random Forest, Gradient Boosting (métricas: Accuracy, F1-macro, AUC-ROC) |
| Clustering | K-Means (k=4) + proyección PCA, Silhouette Score |
| Validación de integridad | Auditoría de columnas y reglas de rango sobre el dataset limpio |
| Dashboard interactivo | KPIs, filtro por tipo de app, gráfico de categorías, scatter Installs vs Reviews, boxplot Rating |
| Informe final | Hallazgos, decisiones técnicas, resultados de negocio y próximos pasos |

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
| _(agregar integrantes)_ | — |

---

## Rama de desarrollo

- `develop` — rama de trabajo activo
- `main` — versión estable para entrega final

---

## Notas

- El notebook es autocontenido: no requiere Docker ni servicios externos.
- Las rutas del dataset se resuelven automáticamente entre rutas locales y Google Colab.
- El dashboard requiere tener las celdas anteriores ejecutadas antes de correr la celda de Dash.