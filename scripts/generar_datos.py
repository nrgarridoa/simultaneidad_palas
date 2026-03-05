"""
Generador de datos sinteticos para el Dashboard de Simultaneidad de Palas.

Simula eventos operativos de 15 palas mineras durante todo el anio 2025,
particionando correctamente por turnos (Dia 08:00-20:00 / Noche 20:00-08:00).
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)

# ==========================
#    CONFIGURACION BASE
# ==========================

PALAS = [f"SH{i:03d}" for i in range(1, 16)]

FECHA_INICIO = datetime(2025, 1, 1, 8, 0)
FECHA_FIN = datetime(2026, 1, 1, 7, 59)

ESTADOS = ["Operativo", "Demora", "Malogrado"]
PROPORCIONES = [0.72, 0.20, 0.08]

SUBTIPOS_DEMORA = ["Espera Camion", "Cambio Turno", "Voladura", "Abastecimiento", "Traslado"]
SUBTIPOS_MALOGRADO = ["PM", "NoPM"]

# Modelos de pala y parametros de produccion
MODELOS_PALA = {
    "P&H 4100XPC": {
        "ton_ciclo": 82,
        "tiempo_ciclo_seg": 50,
        "palas": [f"SH{i:03d}" for i in range(1, 11)],
    },
    "EX5600-6": {
        "ton_ciclo": 65,
        "tiempo_ciclo_seg": 45,
        "palas": [f"SH{i:03d}" for i in range(11, 16)],
    },
}

# Mapa inverso: pala -> modelo y parametros
PALA_CONFIG = {}
for modelo, info in MODELOS_PALA.items():
    for pala in info["palas"]:
        PALA_CONFIG[pala] = {
            "modelo": modelo,
            "ton_ciclo": info["ton_ciclo"],
            "tiempo_ciclo_seg": info["tiempo_ciclo_seg"],
        }


# ===========================
#    FUNCIONES AUXILIARES
# ===========================

def calcular_toneladas(pala, estado, duracion_min):
    """Retorna (produccion, perdida) en toneladas segun estado y duracion."""
    cfg = PALA_CONFIG[pala]
    ciclos = (duracion_min * 60) / cfg["tiempo_ciclo_seg"]
    toneladas = round(ciclos * cfg["ton_ciclo"], 2)
    if estado == "Operativo":
        return toneladas, 0.0
    return 0.0, toneladas


def generar_duracion(estado):
    """Duracion en minutos con distribucion aleatoria segun estado."""
    if estado == "Operativo":
        return max(5, int(np.random.normal(90, 40)))
    elif estado == "Demora":
        return max(5, int(np.random.normal(30, 15)))
    return max(10, int(np.random.exponential(60)))


def obtener_turno(hora):
    """Dia (08:00-19:59) o Noche (20:00-07:59)."""
    return "Dia" if 8 <= hora.hour < 20 else "Noche"


def asignar_subtipo(estado):
    """Subtipo de detencion para Demora y Malogrado."""
    if estado == "Demora":
        return np.random.choice(SUBTIPOS_DEMORA)
    if estado == "Malogrado":
        return np.random.choice(SUBTIPOS_MALOGRADO, p=[0.4, 0.6])
    return ""


def particionar_por_turno(hora_inicio, hora_fin):
    """Corta un intervalo en los limites de turno (08:00, 20:00)."""
    bloques = []
    actual = hora_inicio
    while actual < hora_fin:
        if actual.hour < 8:
            corte = actual.replace(hour=8, minute=0, second=0)
        elif actual.hour < 20:
            corte = actual.replace(hour=20, minute=0, second=0)
        else:
            corte = (actual + timedelta(days=1)).replace(hour=8, minute=0, second=0)

        fin_bloque = min(corte, hora_fin)
        if fin_bloque > actual:
            bloques.append((actual, fin_bloque))
        actual = corte
    return bloques


# ==========================
#   GENERADOR DE EVENTOS
# ==========================

def generar_dia_pala(pala, fecha_inicio):
    """Genera eventos para una pala en un ciclo de 24h (08:00 a 08:00)."""
    eventos = []
    hora_actual = fecha_inicio
    limite = fecha_inicio + timedelta(hours=24)

    while hora_actual < limite:
        estado = np.random.choice(ESTADOS, p=PROPORCIONES)
        duracion = generar_duracion(estado)
        subtipo = asignar_subtipo(estado)

        hora_fin = min(hora_actual + timedelta(minutes=duracion), limite)
        bloques = particionar_por_turno(hora_actual, hora_fin)

        for ini, fin in bloques:
            mins = (fin - ini).total_seconds() / 60
            if mins < 1:
                continue
            prod, perd = calcular_toneladas(pala, estado, mins)
            eventos.append({
                "fecha": ini.strftime("%Y-%m-%d"),
                "hora_inicio": ini.strftime("%H:%M"),
                "hora_fin": fin.strftime("%H:%M"),
                "pala": pala,
                "estado": estado,
                "subtipo": subtipo,
                "turno": obtener_turno(ini),
                "duracion_min": round(mins, 2),
                "duracion_hrs": round(mins / 60, 4),
                "produccion_ton": prod,
                "toneladas_perdidas": perd,
            })

        hora_actual = hora_fin

    return eventos


# ========================
#   EJECUCION PRINCIPAL
# ========================

def main():
    print("Generando eventos para 15 palas, anio completo 2025...")
    todos = []
    fecha = FECHA_INICIO

    total_dias = (FECHA_FIN - FECHA_INICIO).days
    dia_num = 0

    while fecha < FECHA_FIN:
        for pala in PALAS:
            todos.extend(generar_dia_pala(pala, fecha))
        fecha += timedelta(days=1)
        dia_num += 1
        if dia_num % 30 == 0:
            print(f"  {dia_num}/{total_dias} dias procesados...")

    df = pd.DataFrame(todos)

    # Asignar fecha_turno (eventos antes de 08:00 pertenecen al dia anterior)
    hora_num = df["hora_inicio"].str.split(":").str[0].astype(int)
    fecha_dt = pd.to_datetime(df["fecha"])
    df["fecha_turno"] = (fecha_dt - pd.to_timedelta((hora_num < 8).astype(int), unit="D")).dt.strftime("%Y-%m-%d")

    print(f"Total eventos: {len(df)}")

    # ======================
    #    RESUMEN POR PALA
    # ======================
    resumen = df.groupby(["fecha_turno", "pala", "estado"]).agg(
        horas=("duracion_hrs", "sum"),
        produccion=("produccion_ton", "sum"),
        perdida=("toneladas_perdidas", "sum"),
    ).reset_index()

    pivot = resumen.pivot_table(
        index=["fecha_turno", "pala"],
        columns="estado",
        values=["horas", "produccion", "perdida"],
        aggfunc="sum",
        fill_value=0,
    )
    pivot.columns = [f"{v}_{e}" for v, e in pivot.columns]
    pivot = pivot.reset_index()

    for estado in ESTADOS:
        for prefijo in ["horas", "produccion", "perdida"]:
            col = f"{prefijo}_{estado}"
            if col not in pivot.columns:
                pivot[col] = 0.0

    pivot["horas_totales"] = pivot["horas_Operativo"] + pivot["horas_Demora"] + pivot["horas_Malogrado"]
    pivot["disponibilidad_%"] = round(
        (pivot["horas_Operativo"] / pivot["horas_totales"].replace(0, np.nan)) * 100, 2
    ).fillna(0)
    pivot["produccion_total"] = pivot["produccion_Operativo"]
    pivot["perdida_total"] = pivot["perdida_Demora"] + pivot["perdida_Malogrado"]

    cols_num = [c for c in pivot.columns if pivot[c].dtype in ["float64", "float32"]]
    pivot[cols_num] = pivot[cols_num].round(2)
    pivot = pivot.rename(columns={"fecha_turno": "fecha"})

    # ============================
    #    GUARDADO
    # ============================
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(base_dir), "data")
    os.makedirs(data_dir, exist_ok=True)

    df.to_csv(os.path.join(data_dir, "eventos_palas.csv"), index=False)

    cols_resumen = [
        "fecha", "pala",
        "horas_Operativo", "horas_Demora", "horas_Malogrado", "horas_totales",
        "disponibilidad_%",
        "produccion_total", "perdida_total",
        "perdida_Demora", "perdida_Malogrado",
    ]
    pivot[cols_resumen].to_csv(os.path.join(data_dir, "resumen_palas.csv"), index=False)

    print(f"Archivos generados en {data_dir}")
    print(f"  eventos_palas.csv  -> {len(df)} filas")
    print(f"  resumen_palas.csv  -> {len(pivot)} filas")


if __name__ == "__main__":
    main()
