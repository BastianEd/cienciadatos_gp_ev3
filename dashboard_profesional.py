"""
🎯 GOOGLE PLAY STORE - DASHBOARD PROFESIONAL
Evaluación Parcial N°3 | SCY1101 | Duoc UC 2025

Dashboard interactivo con Dash + Plotly
Diseño inspirado en dashboards profesionales (Infrarainodos style)
Paleta: Teal Trust (#028090, #00A896, #02C39A)
"""

import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# 1. CARGAR Y LIMPIAR DATOS
# ═══════════════════════════════════════════════════════════════════════════════

df_raw = pd.read_csv('./data/raw/googleplaystore.csv')

# Limpieza
df = df_raw.copy()
df = df.drop_duplicates(subset=["App"])
df["Rating"] = df["Rating"].fillna(df["Rating"].median())
df["Installs"] = df["Installs"].str.replace("+","").str.replace(",","")
df["Installs"] = pd.to_numeric(df["Installs"], errors="coerce").fillna(0)
df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce").fillna(0)
df["Price"] = df["Price"].str.replace("$","")
df["Price"] = pd.to_numeric(df["Price"], errors="coerce").fillna(0)
df = df.dropna(subset=["App","Category","Type"])
df = df[df["Installs"] > 0]
df = df[(df["Rating"] >= 0) & (df["Rating"] <= 5)]

# Transformaciones adicionales
df["Installs_log"] = np.log1p(df["Installs"])
df["Reviews_log"] = np.log1p(df["Reviews"])
df["Size_MB"] = df["Size"].str.replace("M","").str.replace("k","").astype(float, errors="ignore")

print(f"✓ Dataset limpio: {df.shape}")
print(f"✓ Apps: {len(df)}, Pagadas: {(df['Type']=='Paid').mean()*100:.1f}%")

# ═══════════════════════════════════════════════════════════════════════════════
# 2. PALETA DE COLORES (Teal Trust)
# ═══════════════════════════════════════════════════════════════════════════════

COLORS = {
    "primary": "#028090",      # Teal profundo
    "secondary": "#00A896",    # Seafoam
    "accent": "#02C39A",       # Mint brillante
    "dark": "#1E2761",         # Navy/Dark text
    "white": "#FFFFFF",
    "light": "#F0F8F8",        # Light teal bg
    "success": "#27AE60",      # Verde (Free)
    "info": "#3498DB",         # Azul (Paid)
    "warning": "#E74C3C",      # Rojo (Advertencia)
    "chart1": "#028090",
    "chart2": "#00A896",
    "chart3": "#02C39A",
    "chart4": "#E74C3C",
    "chart5": "#F39C12"
}

# ═══════════════════════════════════════════════════════════════════════════════
# 3. INICIALIZAR APP
# ═══════════════════════════════════════════════════════════════════════════════

app = dash.Dash(
    __name__, 
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://fonts.googleapis.com/css2?family=Cambria:wght@400;700&family=Calibri:wght@400;700&display=swap"
    ]
)

app.title = "Google Play Store Analytics | Evaluación 3"

# ═══════════════════════════════════════════════════════════════════════════════
# 4. ESTILOS GLOBALES
# ═══════════════════════════════════════════════════════════════════════════════

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            * {
                font-family: 'Calibri', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            }
            h1, h2, h3, h4, h5, h6 {
                font-family: 'Cambria', serif;
                font-weight: 700;
                color: #1E2761;
            }
            body {
                background-color: #F8F9FA;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# ═══════════════════════════════════════════════════════════════════════════════
# 5. COMPONENTES: SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════

sidebar = dbc.Col(
    [
        # Logo / Header
        html.Div(
            [
                html.H4("📱 Google Play", style={"color": COLORS["white"], "fontWeight": "700", "marginBottom": "0.5rem"}),
                html.P("Analytics Dashboard", style={"color": COLORS["accent"], "fontSize": "0.9rem", "marginBottom": "1.5rem"})
            ],
            style={"paddingBottom": "1.5rem", "borderBottom": f"2px solid {COLORS['accent']}"}
        ),
        
        # Filtro 1: Categoría
        html.Div(
            [
                html.Label("📂 CATEGORÍA", style={"fontWeight": "700", "fontSize": "0.85rem", "color": COLORS["accent"]}),
                dcc.Dropdown(
                    id='filtro_categoria',
                    options=[{'label': '✓ Todas las Categorías', 'value': 'ALL'}] + 
                            [{'label': f"  {c}", 'value': c} for c in sorted(df['Category'].unique())],
                    value='ALL',
                    clearable=False,
                    style={"fontSize": "0.95rem"},
                    className="mb-4"
                )
            ],
            className="mb-4"
        ),
        
        # Filtro 2: Tipo
        html.Div(
            [
                html.Label("💰 TIPO", style={"fontWeight": "700", "fontSize": "0.85rem", "color": COLORS["accent"]}),
                dcc.Dropdown(
                    id='filtro_tipo',
                    options=[{'label': '✓ Todos los Tipos', 'value': 'ALL'},
                            {'label': '  Free', 'value': 'Free'},
                            {'label': '  Paid', 'value': 'Paid'}],
                    value='ALL',
                    clearable=False,
                    style={"fontSize": "0.95rem"},
                    className="mb-4"
                )
            ],
            className="mb-4"
        ),
        
        # Filtro 3: Rating Mínimo
        html.Div(
            [
                html.Label("⭐ RATING MÍNIMO", style={"fontWeight": "700", "fontSize": "0.85rem", "color": COLORS["accent"]}),
                dcc.RangeSlider(
                    id='filtro_rating',
                    min=0, max=5, step=0.5,
                    value=[0, 5],
                    marks={i: str(i) for i in range(6)},
                    className="mb-4",
                    tooltip={"placement": "bottom", "always_visible": False}
                )
            ],
            className="mb-4"
        ),
        
        # Stats en Sidebar
        html.Hr(style={"borderColor": COLORS["accent"]}),
        
        html.Div(
            [
                html.P("📊 ESTADÍSTICAS GLOBALES", style={"fontWeight": "700", "fontSize": "0.85rem", "color": COLORS["accent"], "marginBottom": "1rem"}),
                
                html.Div(
                    [
                        html.P(f"{len(df):,}", style={"fontSize": "1.8rem", "fontWeight": "700", "color": COLORS["primary"], "marginBottom": "0.2rem"}),
                        html.P("Total Apps", style={"fontSize": "0.8rem", "color": COLORS["dark"]})
                    ],
                    className="mb-3"
                ),
                
                html.Div(
                    [
                        html.P(f"{(df['Type']=='Paid').sum():,}", style={"fontSize": "1.5rem", "fontWeight": "700", "color": COLORS["info"], "marginBottom": "0.2rem"}),
                        html.P("Apps de Pago", style={"fontSize": "0.8rem", "color": COLORS["dark"]})
                    ],
                    className="mb-3"
                ),
                
                html.Div(
                    [
                        html.P(f"{df['Rating'].mean():.2f}/5.0", style={"fontSize": "1.5rem", "fontWeight": "700", "color": COLORS["success"], "marginBottom": "0.2rem"}),
                        html.P("Rating Promedio", style={"fontSize": "0.8rem", "color": COLORS["dark"]})
                    ],
                    className="mb-3"
                ),
            ],
            style={
                "backgroundColor": COLORS["light"],
                "padding": "1rem",
                "borderRadius": "8px",
                "borderLeft": f"4px solid {COLORS['accent']}"
            }
        ),
        
        html.Hr(style={"borderColor": COLORS["accent"], "marginTop": "2rem"}),
        
        html.P(
            "Evaluación Parcial N°3 | SCY1101 | Duoc UC 2025",
            style={"fontSize": "0.7rem", "color": "#999", "textAlign": "center", "marginTop": "2rem"}
        )
    ],
    md=3,
    style={
        "backgroundColor": COLORS["primary"],
        "color": COLORS["white"],
        "padding": "2rem",
        "minHeight": "100vh",
        "boxShadow": f"2px 0 8px rgba(0,0,0,0.1)"
    }
)

# ═══════════════════════════════════════════════════════════════════════════════
# 6. COMPONENTES: KPI CARDS
# ═══════════════════════════════════════════════════════════════════════════════

def crear_kpi_card(titulo, valor, subtitulo, icono, color, ancho="md=3"):
    """Crea una tarjeta KPI profesional"""
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        [
                            html.Span(icono, style={"fontSize": "1.8rem", "marginRight": "0.5rem"}),
                            html.Span(titulo, style={"fontWeight": "700", "fontSize": "0.85rem", "color": COLORS["dark"]})
                        ],
                        style={"display": "flex", "alignItems": "center", "marginBottom": "0.8rem"}
                    ),
                    html.P(valor, style={"fontSize": "2rem", "fontWeight": "700", "color": color, "marginBottom": "0.3rem"}),
                    html.P(subtitulo, style={"fontSize": "0.8rem", "color": "#666", "marginBottom": "0"})
                ],
                style={"padding": "1.5rem"}
            ),
            style={"border": "none", "boxShadow": "0 2px 8px rgba(0,0,0,0.08)", "borderRadius": "8px", "borderTop": f"4px solid {color}"}
        ),
        **{"md": int(ancho.split("=")[1])} if "=" in ancho else {"md": 3},
        className="mb-4"
    )

# ═══════════════════════════════════════════════════════════════════════════════
# 7. LAYOUT PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

app.layout = dbc.Container(
    dbc.Row(
        [
            # SIDEBAR
            sidebar,
            
            # CONTENIDO PRINCIPAL
            dbc.Col(
                [
                    # Header
                    html.Div(
                        [
                            html.H1("Google Play Store Analytics", style={"marginBottom": "0.5rem", "color": COLORS["primary"]}),
                            html.P("Análisis interactivo del ecosistema de aplicaciones móviles", 
                                style={"color": "#666", "fontSize": "1rem", "marginBottom": "0"})
                        ],
                        style={"paddingTop": "2rem", "paddingBottom": "1.5rem", "borderBottom": f"2px solid {COLORS['light']}"}
                    ),
                    
                    # KPI CARDS ROW 1
                    dbc.Row(
                        id='kpi_row',
                        className="mb-4"
                    ),
                    
                    # GRÁFICOS PRINCIPALES
                    dbc.Row(
                        [
                            # Scatter: Installs vs Reviews (GRANDE)
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        dcc.Graph(id='grafico_scatter', style={"height": "500px"}),
                                        style={"padding": "1rem"}
                                    ),
                                    style={"border": "none", "boxShadow": "0 2px 12px rgba(0,0,0,0.08)"}
                                ),
                                md=8,
                                className="mb-4"
                            ),
                            
                            # Columna derecha: 2 gráficos
                            dbc.Col(
                                [
                                    dbc.Card(
                                        dbc.CardBody(
                                            dcc.Graph(id='grafico_free_paid', style={"height": "230px"}),
                                            style={"padding": "1rem"}
                                        ),
                                        style={"border": "none", "boxShadow": "0 2px 12px rgba(0,0,0,0.08)"},
                                        className="mb-4"
                                    ),
                                    dbc.Card(
                                        dbc.CardBody(
                                            dcc.Graph(id='grafico_rating', style={"height": "230px"}),
                                            style={"padding": "1rem"}
                                        ),
                                        style={"border": "none", "boxShadow": "0 2px 12px rgba(0,0,0,0.08)"}
                                    ),
                                ],
                                md=4,
                                className="mb-4"
                            ),
                        ],
                        className="mb-4"
                    ),
                    
                    # GRÁFICOS INFERIORES
                    dbc.Row(
                        [
                            # Categorías
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        dcc.Graph(id='grafico_categorias', style={"height": "400px"}),
                                        style={"padding": "1rem"}
                                    ),
                                    style={"border": "none", "boxShadow": "0 2px 12px rgba(0,0,0,0.08)"}
                                ),
                                md=6,
                                className="mb-4"
                            ),
                            
                            # Content Rating + Precio
                            dbc.Col(
                                [
                                    dbc.Card(
                                        dbc.CardBody(
                                            dcc.Graph(id='grafico_content', style={"height": "190px"}),
                                            style={"padding": "1rem"}
                                        ),
                                        style={"border": "none", "boxShadow": "0 2px 12px rgba(0,0,0,0.08)"},
                                        className="mb-4"
                                    ),
                                    dbc.Card(
                                        dbc.CardBody(
                                            dcc.Graph(id='grafico_precio', style={"height": "190px"}),
                                            style={"padding": "1rem"}
                                        ),
                                        style={"border": "none", "boxShadow": "0 2px 12px rgba(0,0,0,0.08)"}
                                    ),
                                ],
                                md=6,
                                className="mb-4"
                            ),
                        ],
                        className="mb-5"
                    ),
                    
                    # Footer
                    html.Div(
                        html.P(
                            "Dashboard interactivo | Dash + Plotly | Datos de Kaggle",
                            style={"textAlign": "center", "color": "#999", "fontSize": "0.85rem", "paddingTop": "1rem"}
                        ),
                        style={"borderTop": f"1px solid {COLORS['light']}", "marginTop": "2rem", "paddingTop": "1rem"}
                    )
                ],
                md=9,
                style={"padding": "0 2rem", "backgroundColor": "#F8F9FA"}
            )
        ],
        className="g-0"
    ),
    fluid=True,
    style={"margin": "0", "padding": "0", "backgroundColor": "#F8F9FA"}
)

# ═══════════════════════════════════════════════════════════════════════════════
# 8. CALLBACKS - ACTUALIZAR GRÁFICOS
# ═══════════════════════════════════════════════════════════════════════════════

@callback(
    Output('kpi_row', 'children'),
    Output('grafico_scatter', 'figure'),
    Output('grafico_free_paid', 'figure'),
    Output('grafico_rating', 'figure'),
    Output('grafico_categorias', 'figure'),
    Output('grafico_content', 'figure'),
    Output('grafico_precio', 'figure'),
    Input('filtro_categoria', 'value'),
    Input('filtro_tipo', 'value'),
    Input('filtro_rating', 'value')
)
def actualizar_dashboard(cat_sel, tipo_sel, rating_range):
    """Callback principal que actualiza todos los gráficos"""
    
    # Filtrar datos
    dff = df.copy()
    if cat_sel != 'ALL':
        dff = dff[dff['Category'] == cat_sel]
    if tipo_sel != 'ALL':
        dff = dff[dff['Type'] == tipo_sel]
    dff = dff[(dff['Rating'] >= rating_range[0]) & (dff['Rating'] <= rating_range[1])]
    
    # ───────────────────────────────────────────────────────────────────────────
    # KPI CARDS
    # ───────────────────────────────────────────────────────────────────────────
    
    kpi_cards = dbc.Row(
        [
            crear_kpi_card(
                "TOTAL APPS", 
                f"{len(dff):,}",
                f"en la selección",
                "📊",
                COLORS["primary"]
            ),
            crear_kpi_card(
                "FREE/PAID RATIO",
                f"{(dff['Type']=='Free').sum()}/{(dff['Type']=='Paid').sum()}",
                f"{(dff['Type']=='Paid').mean()*100:.1f}% pagadas",
                "💰",
                COLORS["info"]
            ),
            crear_kpi_card(
                "RATING PROMEDIO",
                f"{dff['Rating'].mean():.2f}",
                "de 5.0 estrellas",
                "⭐",
                COLORS["success"]
            ),
            crear_kpi_card(
                "INSTALLS TOTAL",
                f"{(dff['Installs'].sum()/1e9):.1f}B",
                "mil millones",
                "📥",
                COLORS["secondary"]
            ),
        ]
    )
    
    # ───────────────────────────────────────────────────────────────────────────
    # 1. SCATTER: Installs vs Reviews
    # ───────────────────────────────────────────────────────────────────────────
    
# ───────────────────────────────────────────────────────────────────────────
    # 1. SCATTER: Installs vs Reviews (SIN LOG)
    # ───────────────────────────────────────────────────────────────────────────
    
    fig_scatter = px.scatter(
        dff,
        x='Reviews',                    # ← Cambio: sin _log
        y='Installs',                   # ← Cambio: sin _log
        color='Type',
        size='Rating',
        hover_name='App',
        hover_data={'Reviews': ':.0f', 'Installs': ':.0f', 'Rating': ':.2f', 'Type': True},
        color_discrete_map={'Free': COLORS["success"], 'Paid': COLORS["info"]},
        title="Relación: Reviews vs Installs",
        labels={'Reviews': 'Reviews', 'Installs': 'Installs', 'Type': 'Tipo'}  # ← Etiquetas actualizadas
    )
    fig_scatter.update_layout(
        template='plotly_white',
        hovermode='closest',
        height=500,
        font={"family": "Calibri", "size": 12},
        title_font_size=16,
        margin=dict(l=40, r=20, t=60, b=40),
        showlegend=True,
        legend=dict(x=0.02, y=0.98, bgcolor='rgba(255,255,255,0.8)', bordercolor=COLORS["primary"], borderwidth=1)
    )
    # ← Cambio: Agregar escala logarítmica a los ejes (opcional, para mejor visualización con rangos amplios)
    fig_scatter.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.05)',
        type='log'  # Mantiene visual logarítmica pero muestra números reales
    )
    fig_scatter.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.05)',
        type='log'  # Mantiene visual logarítmica pero muestra números reales
    )
    
    # ───────────────────────────────────────────────────────────────────────────
    # 2. PIE: Free vs Paid
    # ───────────────────────────────────────────────────────────────────────────
    
    free_paid = dff['Type'].value_counts().reset_index()
    free_paid.columns = ['Type', 'count']
    
    fig_free_paid = px.pie(
        free_paid,
        names='Type',
        values='count',
        hole=0.4,
        color_discrete_map={'Free': COLORS["success"], 'Paid': COLORS["info"]},
        title="Free vs Paid"
    )
    fig_free_paid.update_traces(
        textposition='auto',
        textfont=dict(size=12, color=COLORS["white"], family="Calibri")
    )
    fig_free_paid.update_layout(
        template='plotly_white',
        height=230,
        font={"family": "Calibri", "size": 11},
        title_font_size=14,
        margin=dict(l=20, r=20, t=50, b=20),
        showlegend=True,
        legend=dict(x=0.7, y=0.9)
    )
    
    # ───────────────────────────────────────────────────────────────────────────
    # 3. HISTOGRAM: Rating Distribution
    # ───────────────────────────────────────────────────────────────────────────
    
    fig_rating = px.histogram(
        dff,
        x='Rating',
        nbins=20,
        title="Distribución de Rating",
        color_discrete_sequence=[COLORS["primary"]]
    )
    fig_rating.update_layout(
        template='plotly_white',
        showlegend=False,
        height=230,
        font={"family": "Calibri", "size": 11},
        title_font_size=14,
        margin=dict(l=40, r=20, t=50, b=40),
        yaxis_title="Apps",
        xaxis_title="Rating"
    )
    fig_rating.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.05)')
    fig_rating.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.05)')
    
    # ───────────────────────────────────────────────────────────────────────────
    # 4. BAR HORIZONTAL: Top Categorías
    # ───────────────────────────────────────────────────────────────────────────
    
    top_cats = dff['Category'].value_counts().head(10).reset_index()
    top_cats.columns = ['Category', 'count']
    
    fig_cats = px.bar(
        top_cats,
        y='Category',
        x='count',
        orientation='h',
        title="Top 10 Categorías",
        color_discrete_sequence=[COLORS["secondary"]]
    )
    fig_cats.update_layout(
        template='plotly_white',
        showlegend=False,
        height=400,
        font={"family": "Calibri", "size": 11},
        title_font_size=14,
        margin=dict(l=100, r=20, t=50, b=40),
        xaxis_title="Apps",
        yaxis_title="",
        yaxis={"categoryorder": "total ascending"}
    )
    fig_cats.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.05)')
    
    # ───────────────────────────────────────────────────────────────────────────
    # 5. BAR: Content Rating
    # ───────────────────────────────────────────────────────────────────────────
    
    content_counts = dff['Content Rating'].value_counts().reset_index()
    content_counts.columns = ['Content Rating', 'count']
    
    fig_content = px.bar(
        content_counts,
        x='Content Rating',
        y='count',
        title="Apps por Público",
        color_discrete_sequence=[COLORS["accent"]]
    )
    fig_content.update_layout(
        template='plotly_white',
        showlegend=False,
        height=190,
        font={"family": "Calibri", "size": 10},
        title_font_size=14,
        margin=dict(l=40, r=20, t=50, b=40),
        yaxis_title=""
    )
    fig_content.update_xaxes(tickangle=-45)
    fig_content.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.05)')
    
    # ───────────────────────────────────────────────────────────────────────────
    # 6. BOX: Precio (solo apps pagadas)
    # ───────────────────────────────────────────────────────────────────────────
    
    dff_paid = dff[dff['Type'] == 'Paid']
    
    if len(dff_paid) > 0:
        fig_precio = px.box(
            dff_paid,
            y='Price',
            title="Distribución de Precios (Paid)",
            color_discrete_sequence=[COLORS["chart4"]]
        )
    else:
        fig_precio = go.Figure()
        fig_precio.add_annotation(text="Sin datos de apps pagadas", x=0.5, y=0.5, showarrow=False)
        fig_precio.update_layout(title="Distribución de Precios (Paid)")
    
    fig_precio.update_layout(
        template='plotly_white',
        showlegend=False,
        height=190,
        font={"family": "Calibri", "size": 10},
        title_font_size=14,
        margin=dict(l=40, r=20, t=50, b=40),
        yaxis_title="Precio ($)"
    )
    fig_precio.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.05)')
    
    return kpi_cards, fig_scatter, fig_free_paid, fig_rating, fig_cats, fig_content, fig_precio

# ═══════════════════════════════════════════════════════════════════════════════
# 9. RUN SERVER
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("🚀 Dashboard iniciando en http://127.0.0.1:8050")
    print(f"✓ Dataset: {len(df):,} apps | Rating: {df['Rating'].mean():.2f}/5.0")
    app.run(debug=True, host='127.0.0.1', port=8050)
