import pandas as pd
import numpy as np
import dash
from dash import dcc, html, dash_table, ctx, callback_context
from dash.dependencies import Input, Output, State
from dash.dcc import send_data_frame
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# =============================
# 1. Cargar Data
# =============================
df_eventos = pd.read_csv("data/eventos_palas.csv")
df_resumen = pd.read_csv("data/resumen_palas.csv")

# Datetimes completos para el Gantt
fecha_dt = pd.to_datetime(df_eventos["fecha"])
df_eventos["datetime_inicio"] = fecha_dt + pd.to_timedelta(df_eventos["hora_inicio"] + ":00")
df_eventos["datetime_fin"] = fecha_dt + pd.to_timedelta(df_eventos["hora_fin"] + ":00")

# Corregir eventos que cruzan medianoche
mask_cruza = df_eventos["datetime_fin"] <= df_eventos["datetime_inicio"]
df_eventos.loc[mask_cruza, "datetime_fin"] += pd.Timedelta(days=1)

FECHAS_DISPONIBLES = sorted(df_eventos["fecha_turno"].unique())
PALAS_DISPONIBLES = sorted(df_eventos["pala"].unique())

COLOR_MAP = {
    "Operativo": "#87BD45",
    "Demora": "#FFAA01",
    "Malogrado": "#EB5546",
}

# Pala -> modelo (SH001-SH010: P&H 4100XPC, SH011-SH015: EX5600-6)
PALA_MODELO = {}
for i in range(1, 11):
    PALA_MODELO[f"SH{i:03d}"] = "P&H 4100XPC"
for i in range(11, 16):
    PALA_MODELO[f"SH{i:03d}"] = "EX5600-6"

BUDGET_RATES = {
    "P&H 4100XPC": 82 * 3600 / 50,  # ton/hora
    "EX5600-6": 65 * 3600 / 45,
}

# =============================
# 2. Inicializar la App
# =============================
app = dash.Dash(__name__)
app.title = "Simultaneidad de Palas"
server = app.server

# =============================
# 3. Layout
# =============================
app.layout = html.Div([

    # --- HEADER ---
    html.Div([
        html.Div([
            html.H1("Simultaneidad Palas", className="header-title")
        ], style={"flex": "1"}),
        html.Div([
            html.Div(id="header-timestamp", className="header-timestamp"),
        ], style={"flex": "1", "textAlign": "center", "display": "none"}),
        html.Div([
            html.H4("NILSON R. GARRIDO ASENJO",
                     style={"margin": "0", "fontWeight": "bold", "color": "#FFFFFF"}),
            html.P("MINING ENGINEER | DATA ANALYST | PYTHON DEVELOPER",
                    style={"margin": "2px 0", "fontSize": "12px", "color": "#E0F2F1"}),
            html.A("nrgarridoa.github.io", href="https://nrgarridoa.github.io",
                    target="_blank",
                    style={"fontSize": "12px", "color": "#B2DFDB", "textDecoration": "none"})
        ], style={"textAlign": "right"})
    ], className="header-container"),

    # --- FILTROS: Fecha con flechas + Pala ---
    html.Div([
        html.Div([
            html.Label("Fecha:"),
            html.Div([
                html.Button("\u276E", id="btn-fecha-prev", className="btn-nav", n_clicks=0),
                dcc.Dropdown(
                    id="filtro-fecha",
                    options=[{"label": f, "value": f} for f in FECHAS_DISPONIBLES],
                    value=FECHAS_DISPONIBLES[0],
                    clearable=False,
                    className="fecha-dropdown",
                ),
                html.Button("\u276F", id="btn-fecha-next", className="btn-nav", n_clicks=0),
            ], className="fecha-nav-group"),
        ], className="filtro-fecha-wrapper"),
        html.Div([
            html.Label("Filtrar Pala:"),
            dcc.Dropdown(
                id="filtro-pala",
                options=[{"label": p, "value": p} for p in PALAS_DISPONIBLES],
                value=None, placeholder="Todas las palas",
                multi=True, style={"width": "100%"},
            )
        ], style={"flex": "2", "minWidth": "300px"}),
    ], className="filters-bar"),

    # --- GANTT ---
    html.Div([
        html.Div([
            html.H3("Estados Equipos", className="section-title"),
            html.Div([
                html.Span("Estado:", style={"fontWeight": "600", "marginRight": "12px", "color": "#5A6B8A"}),
                html.Span("\u25A0", style={"color": COLOR_MAP["Demora"], "fontSize": "18px", "marginRight": "4px"}),
                html.Span("Demora", style={"marginRight": "16px", "fontSize": "13px"}),
                html.Span("\u25A0", style={"color": COLOR_MAP["Malogrado"], "fontSize": "18px", "marginRight": "4px"}),
                html.Span("Malogrado", style={"marginRight": "16px", "fontSize": "13px"}),
                html.Span("\u25A0", style={"color": COLOR_MAP["Operativo"], "fontSize": "18px", "marginRight": "4px"}),
                html.Span("Operativo", style={"fontSize": "13px"}),
            ], className="legend-bar"),
        ], className="gantt-header"),

        html.Div(id="gantt-fecha-label", className="gantt-fecha-label"),
        dcc.Graph(id="grafico-gantt", config={"displayModeBar": False}),
    ], className="gantt-section"),

    # --- KPIs ---
    html.Div([
        html.Div([
            html.Div(html.Span("\u2699", style={"fontSize": "28px"}), className="kpi-icon-box kpi-green"),
            html.Div([
                html.P("Disponibilidad Promedio", className="kpi-label"),
                html.H2(id="kpi-disponibilidad", className="kpi-value"),
            ])
        ], className="kpi-card"),
        html.Div([
            html.Div(html.Span("\u26A0", style={"fontSize": "28px"}), className="kpi-icon-box kpi-red"),
            html.Div([
                html.P("Toneladas Perdidas", className="kpi-label"),
                html.H2(id="kpi-perdidas", className="kpi-value"),
            ])
        ], className="kpi-card"),
        html.Div([
            html.Div(html.Span("\u23F1", style={"fontSize": "28px"}), className="kpi-icon-box kpi-blue"),
            html.Div([
                html.P("Horas Operativas", className="kpi-label"),
                html.H2(id="kpi-horas", className="kpi-value"),
            ])
        ], className="kpi-card"),
        html.Div([
            html.Div(html.Span("\u25B2", style={"fontSize": "28px"}), className="kpi-icon-box kpi-orange"),
            html.Div([
                html.P("Palas Detenidas", className="kpi-label"),
                html.H2(id="kpi-detenidas", className="kpi-value"),
            ])
        ], className="kpi-card"),
    ], className="kpi-container"),

    # --- TABLAS ---
    html.Div([
        # Resumen Detenciones (solo palas con Malogrado)
        html.Div([
            html.Div([
                html.H3("Resumen Detenciones de Palas", className="table-title"),
                html.Span("Total en Horas", className="table-subtitle"),
                html.Button("Descargar", id="btn-exportar", n_clicks=0, className="btn-export"),
                dcc.Download(id="descarga-datos"),
            ], className="table-header-row"),
            html.Div(id="tabla-resumen-container"),
        ], className="table-panel"),

        # Detalle Detenciones (estilo Antamina con filtro tipo detencion)
        html.Div([
            html.Div([
                html.H3("Detalle Detenciones de Palas", className="table-title"),
                html.Span("Total en Horas", className="table-subtitle"),
                html.Div([
                    html.Label("Tipo de Detencion:", style={"fontSize": "11px", "fontWeight": "600", "marginRight": "6px"}),
                    dcc.Dropdown(
                        id="filtro-tipo-detencion",
                        options=[
                            {"label": "Todos", "value": "Todos"},
                            {"label": "PM", "value": "PM"},
                            {"label": "NoPM", "value": "NoPM"},
                        ],
                        value="Todos",
                        clearable=False,
                        style={"width": "120px", "fontSize": "12px"},
                    ),
                ], className="tipo-detencion-filter"),
            ], className="table-header-row"),
            html.Div(id="tabla-detalle-container"),
        ], className="table-panel"),
    ], className="tables-container"),

], className="app-wrapper")


# ===============================
# 4. Callbacks
# ===============================

# --- Navegacion de fecha con flechas ---
@app.callback(
    Output("filtro-fecha", "value"),
    Input("btn-fecha-prev", "n_clicks"),
    Input("btn-fecha-next", "n_clicks"),
    State("filtro-fecha", "value"),
    prevent_initial_call=True,
)
def navegar_fecha(prev_clicks, next_clicks, fecha_actual):
    trigger = ctx.triggered_id
    idx = FECHAS_DISPONIBLES.index(fecha_actual)
    if trigger == "btn-fecha-prev":
        idx = max(0, idx - 1)
    elif trigger == "btn-fecha-next":
        idx = min(len(FECHAS_DISPONIBLES) - 1, idx + 1)
    return FECHAS_DISPONIBLES[idx]


# --- Timestamp ---
@app.callback(
    Output("header-timestamp", "children"),
    Input("filtro-fecha", "value"),
)
def actualizar_timestamp(fecha):
    return f"Fecha seleccionada: {fecha}"


# --- Fecha label Gantt ---
@app.callback(
    Output("gantt-fecha-label", "children"),
    Input("filtro-fecha", "value"),
)
def actualizar_gantt_fecha(fecha):
    return fecha


# --- Compactar bloques consecutivos del mismo estado ---
def compactar_bloques(df_turno):
    TOL = 60
    bloques = []
    for pala, g in df_turno.sort_values(["pala", "start_clip"]).groupby("pala", sort=False):
        prev_estado, ini, fin = None, None, None
        for _, row in g.iterrows():
            if prev_estado is None:
                ini, fin, prev_estado = row["start_clip"], row["end_clip"], row["estado"]
            elif row["estado"] == prev_estado and abs((row["start_clip"] - fin).total_seconds()) <= TOL:
                fin = max(fin, row["end_clip"])
            else:
                bloques.append({"pala": pala, "estado": prev_estado, "start_clip": ini, "end_clip": fin})
                ini, fin, prev_estado = row["start_clip"], row["end_clip"], row["estado"]
        if prev_estado is not None:
            bloques.append({"pala": pala, "estado": prev_estado, "start_clip": ini, "end_clip": fin})
    if bloques:
        return pd.DataFrame(bloques)
    return pd.DataFrame(columns=["pala", "estado", "start_clip", "end_clip"])


# --- Gantt unificado con subplots ---
@app.callback(
    Output("grafico-gantt", "figure"),
    Input("filtro-fecha", "value"),
    Input("filtro-pala", "value"),
)
def actualizar_gantt(fecha, palas):
    fecha_base = pd.to_datetime(fecha)
    palas_orden = list(palas) if palas else list(PALAS_DISPONIBLES)
    n_palas = len(palas_orden)
    pala_to_y = {p: (n_palas - 1 - i) for i, p in enumerate(palas_orden)}

    BAR_H = 30
    fig_height = max(320, n_palas * BAR_H + 100)

    fig = make_subplots(
        rows=1, cols=2,
        shared_yaxes=True,
        column_widths=[0.5, 0.5],
        horizontal_spacing=0.015,
        subplot_titles=["Dia", "Noche"],
    )

    dia_start = fecha_base.replace(hour=8, minute=0)
    dia_end = fecha_base.replace(hour=20, minute=0)
    noche_start = fecha_base.replace(hour=20, minute=0)
    noche_end = fecha_base + pd.Timedelta(hours=32)

    legend_shown = set()

    for col_idx, (t_start, t_end) in enumerate(
        [(dia_start, dia_end), (noche_start, noche_end)], start=1
    ):
        mask = (df_eventos["datetime_fin"] > t_start) & (df_eventos["datetime_inicio"] < t_end)
        df_f = df_eventos.loc[mask].copy()

        if palas:
            df_f = df_f[df_f["pala"].isin(palas)]

        df_f["start_clip"] = df_f["datetime_inicio"].clip(lower=t_start, upper=t_end)
        df_f["end_clip"] = df_f["datetime_fin"].clip(lower=t_start, upper=t_end)
        df_f = df_f[df_f["end_clip"] > df_f["start_clip"]]

        if df_f.empty:
            continue

        df_comp = compactar_bloques(df_f)

        for estado in ["Operativo", "Demora", "Malogrado"]:
            df_est = df_comp[df_comp["estado"] == estado]
            if df_est.empty:
                continue

            show_leg = estado not in legend_shown
            legend_shown.add(estado)

            for _, row in df_est.iterrows():
                y_val = pala_to_y.get(row["pala"])
                if y_val is None:
                    continue
                fig.add_trace(
                    go.Bar(
                        x=[(row["end_clip"] - row["start_clip"]).total_seconds() * 1000],
                        y=[y_val],
                        base=[row["start_clip"].timestamp() * 1000],
                        orientation="h",
                        marker_color=COLOR_MAP[estado],
                        marker_line_width=0.5,
                        marker_line_color=COLOR_MAP[estado],
                        opacity=0.92,
                        width=1.0,
                        name=estado,
                        legendgroup=estado,
                        showlegend=show_leg,
                        hovertemplate=(
                            f"<b>{row['pala']}</b> - {estado}<br>"
                            f"{row['start_clip'].strftime('%H:%M')} - "
                            f"{row['end_clip'].strftime('%H:%M')}<extra></extra>"
                        ),
                    ),
                    row=1, col=col_idx,
                )
                show_leg = False

    # Ejes Y
    y_ticks = list(range(n_palas))
    y_labels = list(reversed(palas_orden))

    fig.update_yaxes(
        tickvals=y_ticks, ticktext=y_labels,
        tickfont=dict(size=11, color="#2C3E50"),
        showgrid=False, showline=False, zeroline=False,
        range=[-0.5, n_palas - 0.5],
        fixedrange=True, title="Equipo",
        row=1, col=1,
    )
    fig.update_yaxes(
        tickvals=y_ticks, ticktext=[""] * n_palas,
        range=[-0.5, n_palas - 0.5],
        fixedrange=True,
        showgrid=False, showline=False, zeroline=False,
        row=1, col=2,
    )

    # Ejes X
    for col_idx, (t_start, t_end) in enumerate(
        [(dia_start, dia_end), (noche_start, noche_end)], start=1
    ):
        fig.update_xaxes(
            type="date",
            range=[t_start.timestamp() * 1000, t_end.timestamp() * 1000],
            tickformat="%I:%M %p",
            dtick=2 * 3600 * 1000,
            showgrid=False, zeroline=False, showline=False,
            fixedrange=True,
            row=1, col=col_idx,
        )

    fig.update_layout(
        height=fig_height,
        margin=dict(l=10, r=10, t=30, b=10),
        plot_bgcolor="white", paper_bgcolor="white",
        barmode="overlay", bargap=0,
        showlegend=False,
        font=dict(family="Segoe UI, sans-serif"),
    )

    # Etiqueta "Cambio de Turno" entre los dos paneles
    fig.add_annotation(
        text="Cambio de Turno",
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        textangle=-90,
        font=dict(size=11, color="#004D40", family="Segoe UI"),
        opacity=0.7,
    )

    for ann in fig.layout.annotations:
        if hasattr(ann, "text") and ann.text in ["Dia", "Noche"]:
            ann.update(font=dict(size=14, color="#004D40", family="Segoe UI"), font_weight="bold")

    return fig


# --- KPIs (consistente: Malogrado = detenida) ---
@app.callback(
    Output("kpi-disponibilidad", "children"),
    Output("kpi-perdidas", "children"),
    Output("kpi-horas", "children"),
    Output("kpi-detenidas", "children"),
    Input("filtro-fecha", "value"),
    Input("filtro-pala", "value"),
)
def actualizar_kpis(fecha, palas):
    df_f = df_eventos[df_eventos["fecha_turno"] == fecha]
    if palas:
        df_f = df_f[df_f["pala"].isin(palas)]

    total_horas = df_f["duracion_hrs"].sum()
    horas_op = df_f.loc[df_f["estado"] == "Operativo", "duracion_hrs"].sum()
    perdidas = df_f["toneladas_perdidas"].sum()
    disponibilidad = (horas_op / total_horas) * 100 if total_horas > 0 else 0

    # Detenidas = palas con al menos un evento Malogrado
    palas_detenidas = df_f.loc[df_f["estado"] == "Malogrado", "pala"].nunique()

    return (
        f"{disponibilidad:.1f}%",
        f"{int(perdidas):,} ton",
        f"{horas_op:.1f} h",
        str(palas_detenidas),
    )


# --- Tabla Resumen: solo palas con Malogrado (alineado con KPI y detalle) ---
@app.callback(
    Output("tabla-resumen-container", "children"),
    Input("filtro-fecha", "value"),
    Input("filtro-pala", "value"),
)
def actualizar_tabla_resumen(fecha, palas):
    df_f = df_eventos[df_eventos["fecha_turno"] == fecha]
    if palas:
        df_f = df_f[df_f["pala"].isin(palas)]

    # Solo palas con al menos un evento Malogrado
    palas_mal = sorted(df_f.loc[df_f["estado"] == "Malogrado", "pala"].unique())
    if not palas_mal:
        return html.P(
            "Sin detenciones por falla en esta fecha.",
            style={"textAlign": "center", "color": "#7F8C8D", "padding": "20px"},
        )

    # Horas Malogrado por pala
    df_mal = df_f[(df_f["pala"].isin(palas_mal)) & (df_f["estado"] == "Malogrado")]
    hrs_por_pala = df_mal.groupby("pala")["duracion_hrs"].sum().round(2)

    n_palas = len(palas_mal)
    total_hrs = hrs_por_pala.sum()

    # Perdida por modelo
    df_mal_m = df_mal.copy()
    df_mal_m["modelo"] = df_mal_m["pala"].map(PALA_MODELO)
    perdida_modelo = df_mal_m.groupby("modelo")["toneladas_perdidas"].sum().round(0)

    rows = [
        html.Tr([
            html.Th("N\u00B0 Palas", style={"textAlign": "left", "padding": "6px 12px"}),
            html.Th(fecha, style={"textAlign": "right", "padding": "6px 12px"}),
        ], className="resumen-header-row"),
        html.Tr([
            html.Td(str(n_palas), style={"textAlign": "center", "padding": "6px 12px", "fontWeight": "700"}),
            html.Td(f"{total_hrs:.2f}", style={"textAlign": "right", "padding": "6px 12px", "fontWeight": "700"}),
        ]),
        html.Tr([html.Td(colSpan=2, style={"height": "12px"})]),
    ]

    for modelo, ton in perdida_modelo.items():
        rows.append(html.Tr([
            html.Td(f"Perdida {modelo} (Ton)", style={"textAlign": "left", "padding": "6px 12px", "fontWeight": "600"}),
            html.Td(f"{int(ton):,}", style={"textAlign": "right", "padding": "6px 12px", "fontWeight": "700", "color": "#C0392B"}),
        ]))

    return html.Table(rows, className="resumen-table")


# --- Tabla Detalle: Fecha, Descripcion, Budget, PM, NoPM, Total ---
@app.callback(
    Output("tabla-detalle-container", "children"),
    Input("filtro-fecha", "value"),
    Input("filtro-pala", "value"),
    Input("filtro-tipo-detencion", "value"),
)
def actualizar_tabla_detalle(fecha, palas, tipo_detencion):
    df_f = df_eventos[
        (df_eventos["fecha_turno"] == fecha) & (df_eventos["estado"] == "Malogrado")
    ]
    if palas:
        df_f = df_f[df_f["pala"].isin(palas)]
    if tipo_detencion and tipo_detencion != "Todos":
        df_f = df_f[df_f["subtipo"] == tipo_detencion]

    if df_f.empty:
        return html.P(
            "Sin detenciones por falla en esta fecha.",
            style={"textAlign": "center", "color": "#7F8C8D", "padding": "20px"},
        )

    df_f = df_f.copy()
    df_f["modelo"] = df_f["pala"].map(PALA_MODELO)
    df_f["descripcion"] = df_f["pala"] + " (" + df_f["modelo"] + ")"

    # Pivot horas por pala y subtipo
    pivot_hrs = df_f.groupby(["descripcion", "subtipo"])["duracion_hrs"].sum().unstack(fill_value=0)
    for col in ["PM", "NoPM"]:
        if col not in pivot_hrs.columns:
            pivot_hrs[col] = 0.0
    pivot_hrs["Total"] = pivot_hrs.sum(axis=1)
    pivot_hrs = pivot_hrs.round(2).reset_index()

    total_pm = pivot_hrs["PM"].sum()
    total_nopm = pivot_hrs["NoPM"].sum()
    total_total = pivot_hrs["Total"].sum()
    n_equipos = len(pivot_hrs)

    # Perdida por modelo
    perd_modelo = df_f.groupby("modelo").agg(
        horas=("duracion_hrs", "sum"),
        perdida=("toneladas_perdidas", "sum"),
    ).reset_index()
    perd_modelo["budget"] = perd_modelo.apply(
        lambda r: round(r["horas"] * BUDGET_RATES.get(r["modelo"], 0), 0), axis=1
    )

    # Construir tabla HTML
    header = html.Tr([
        html.Th("Fecha", style={"width": "80px"}),
        html.Th("Descripcion"),
        html.Th("Budget"),
        html.Th("PM"),
        html.Th("NoPM"),
        html.Th("Total"),
        html.Th(str(n_equipos), style={"width": "40px"}),
    ], className="detalle-header-row")

    body = []
    first = True
    for _, row in pivot_hrs.sort_values("descripcion").iterrows():
        body.append(html.Tr([
            html.Td(fecha if first else "", style={"fontWeight": "600" if first else "normal"}),
            html.Td(row["descripcion"], style={"textAlign": "left"}),
            html.Td(""),
            html.Td(f"{row['PM']:.2f}" if row["PM"] > 0 else ""),
            html.Td(f"{row['NoPM']:.2f}" if row["NoPM"] > 0 else ""),
            html.Td(f"{row['Total']:.2f}", style={"fontWeight": "700"}),
            html.Td(f"{row['Total']:.2f}", style={"fontWeight": "700"}),
        ]))
        first = False

    # Total Equipos
    body.append(html.Tr([
        html.Td(""),
        html.Td("Total Equipos (Hrs)", style={"textAlign": "left", "fontWeight": "700"}),
        html.Td(""),
        html.Td(f"{total_pm:.2f}" if total_pm > 0 else "", style={"fontWeight": "700"}),
        html.Td(f"{total_nopm:.2f}" if total_nopm > 0 else "", style={"fontWeight": "700"}),
        html.Td(f"{total_total:.2f}", style={"fontWeight": "700"}),
        html.Td(f"{total_total:.2f}", style={"fontWeight": "700"}),
    ], className="detalle-total-row"))

    body.append(html.Tr([html.Td(colSpan=7, style={"height": "8px", "borderBottom": "none"})]))

    # Perdida por modelo
    for _, row in perd_modelo.iterrows():
        body.append(html.Tr([
            html.Td(""),
            html.Td(f"Perdida {row['modelo']} (Ton)", style={"textAlign": "left", "fontWeight": "600"}),
            html.Td(f"{int(row['budget']):,}", style={"fontWeight": "600"}),
            html.Td("", colSpan=2),
            html.Td(f"{int(row['perdida']):,}", style={"fontWeight": "700", "color": "#C0392B"}),
            html.Td(f"{int(row['perdida']):,}", style={"fontWeight": "700", "color": "#C0392B"}),
        ], className="detalle-perdida-row"))

    return html.Table([html.Thead(header), html.Tbody(body)], className="detalle-table")


# --- Exportar ---
@app.callback(
    Output("descarga-datos", "data"),
    Input("btn-exportar", "n_clicks"),
    State("filtro-fecha", "value"),
    State("filtro-pala", "value"),
    prevent_initial_call=True,
)
def exportar_datos(n_clicks, fecha, palas):
    if ctx.triggered_id != "btn-exportar":
        return dash.no_update

    df_t = df_resumen.copy()
    if fecha:
        df_t = df_t[df_t["fecha"] == fecha]
    if palas:
        df_t = df_t[df_t["pala"].isin(palas)]

    nombre = f"resumen_palas_{fecha}.csv" if fecha else "resumen_palas.csv"
    return send_data_frame(df_t.to_csv, filename=nombre, index=False)


# ===============================
# 5. Ejecutar
# ===============================
if __name__ == "__main__":
    app.run(debug=True)
