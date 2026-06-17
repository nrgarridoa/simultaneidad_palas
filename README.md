![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Dash](https://img.shields.io/badge/Dash-008DE4?style=for-the-badge&logo=plotly&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=black)

#### Si te resulta útil este proyecto, apóyalo con un [![Star](https://img.shields.io/github/stars/nrgarridoa/simultaneidad_palas?style=social)](https://github.com/nrgarridoa/simultaneidad_palas/stargazers) en el repositorio.

---

# Dashboard de Simultaneidad de Palas - Monitoreo de Carguío

> **En gran minería a cielo abierto, cada hora de pala detenida son miles de toneladas que no se mueven. En esta operación las detenciones representan ~109.8 millones de toneladas no producidas al año, y el 56% son demoras operativas evitables, no fallas de equipo.**

Este dashboard transforma los registros de eventos operativos de una flota de palas
en inteligencia de carguío. Permite a jefes de mina, despachadores y superintendentes
de operaciones **tomar decisiones basadas en datos** sobre la disponibilidad de los
equipos, las causas de detención y las pérdidas de producción en cada turno.

[![Ver Dashboard en Vivo](https://img.shields.io/badge/Ver%20Dashboard%20en%20Vivo-Render-46E3B7?style=for-the-badge&logo=render&logoColor=black)](https://simultaneidad-palas.onrender.com)

---

## Vista previa

| Dashboard general | Gantt Día / Noche |
|:---:|:---:|
| ![Dashboard](screenshots/dashboard.png) | ![Gantt](screenshots/gantt.png) |

| KPIs operativos | Detalle de detenciones |
|:---:|:---:|
| ![KPIs](screenshots/kpis.png) | ![Detalle](screenshots/detalle.png) |

---

## Qué problema resuelve

| Sin este dashboard | Con este dashboard |
|---|---|
| La disponibilidad se revisa al cierre de turno o de mes | Disponibilidad en tiempo real por pala, modelo y fecha |
| No se ve qué palas operan en simultáneo ni cuáles están detenidas | Gantt día/noche con el estado de cada equipo, hora a hora |
| Las demoras operativas se mezclan con las fallas | Separación clara entre Demora, Malogrado (PM/NoPM) y Operativo |
| No se cuantifica la pérdida de producción | Toneladas perdidas por estado, modelo y período |
| Cada área maneja su propio reporte | Una sola fuente de verdad, filtrable y exportable a CSV |

---

## Hallazgos clave

Los datos revelan patrones críticos para la gestión del carguío:

**1. La disponibilidad está al límite del benchmark**
- Disponibilidad promedio de la flota: **85.3%** (benchmark típico 85%)
- El **14.7%** del tiempo las palas no están produciendo (Demora + Malogrado)

**2. Las demoras operativas pesan más que las fallas**
- Pérdidas por **Demora**: **61.3M ton** (56%)
- Pérdidas por **Malogrado** (fallas): **48.5M ton** (44%)
- La mayor oportunidad está en la gestión operativa (esperas, voladura, traslados), no solo en mantenimiento

**3. El mantenimiento es mayormente reactivo**
- Detenciones **NoPM** (no programadas): **5,098 hrs**
- Detenciones **PM** (programadas): **3,450 hrs**
- Ratio ~**60/40 reactivo**: oportunidad clara para mantenimiento preventivo

**4. La flota P&H concentra la mayor pérdida**
- P&H 4100XPC: **76.5M ton** perdidas (70% del total)
- EX5600-6: **33.3M ton** perdidas (30%)
- Por ser flota mayor (10 de 15 palas) y de mayor capacidad: foco para priorizar intervenciones

---

## Secciones del dashboard

### Gantt Día / Noche
Línea de tiempo del estado de cada pala dividida en los dos turnos (Día 08:00-20:00,
Noche 20:00-08:00). Cada barra es un bloque de estado (Operativo, Demora, Malogrado)
con tooltip de horario. Permite ver de un vistazo cuántas palas operan en simultáneo
y cuáles están detenidas en cada momento.

### KPIs operativos
Cuatro indicadores en tiempo real que responden al filtro de fecha y pala:
disponibilidad promedio, toneladas perdidas, horas operativas y número de palas
detenidas.

### Tabla resumen de detenciones
Resumen de las palas con falla en la fecha seleccionada, con horas de detención y
pérdida de producción desglosada por modelo de equipo.

### Tabla detalle de detenciones
Desglose por equipo con horas PM, NoPM y total, más el budget de producción y las
toneladas perdidas por modelo. Incluye filtro por tipo de detención (Todos / PM / NoPM).

### Navegación y exportación
Navegación por fecha con flechas, filtro múltiple por pala y exportación a CSV de los
datos filtrados.

---

## Contexto de la operación

| Parámetro | Valor |
|---|---|
| **Tipo de operación** | Tajo abierto (open pit) |
| **Flota** | 15 palas: 10 P&H 4100XPC, 5 EX5600-6 |
| **Turnos** | Día (08:00-20:00) y Noche (20:00-08:00) |
| **Estados** | Operativo, Demora, Malogrado (PM / NoPM) |
| **Período** | Año completo 2025 (365 días) |
| **Volumen de datos** | ~113,800 eventos operativos + 5,475 resúmenes diarios |
| **Datos** | Sintéticos generados con distribuciones realistas (seed=42) |

---

## Autor

### Nilson Rolando Garrido Asenjo

**Mining Engineer | Data Analyst | Python Developer**

[![Portfolio](https://img.shields.io/badge/Portfolio-nrgarridoa.github.io-0068FF?style=for-the-badge&logo=github&logoColor=white)](https://nrgarridoa.github.io)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-nrgarridoa-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/nrgarridoa)
[![YouTube](https://img.shields.io/badge/YouTube-nrgarridoa-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@nrgarridoa)
[![Gmail](https://img.shields.io/badge/Gmail-nrgarridoa@gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:nrgarridoa@gmail.com)

Ingeniero de Minas (UNC, primer puesto) y Administrador Industrial (SENATI) con trayectoria en gran minería, industria farmacéutica y manufactura de alimentos. He liderado equipos de campo en Newmont Yanacocha, Gold Fields y Silver Mountain, dirigido proyectos tecnológicos en CODE UNI y ejecutado consultoría de reconciliación de mineral para Chinalco y reportabilidad operativa en gran minería.

Mi enfoque es transformar datos operativos en inteligencia para la toma de decisiones, combinando experiencia de campo con herramientas como Power BI, Python, SQL y DAX. Piloto de drones con operaciones en superficie (fotogrametría, volumetría) y en subterránea (LiDAR con Elios 3 para Flyability). Docente de Power BI y Python aplicado a minería.

Formación continua en Platzi, Coursera, iSE-Latam y Netzun en analítica de datos, programación, gestión ágil de proyectos y tecnologías mineras.

[![GitHub](https://img.shields.io/badge/GitHub-nrgarridoa-black?style=for-the-badge&logo=github&logoColor=white)](https://github.com/nrgarridoa)

---

<details>
<summary><strong>Documentación Técnica (clic para expandir)</strong></summary>

## Modelo de datos

Dos datasets sintéticos que alimentan el dashboard:

| Tabla | Registros | Descripción |
|---|---|---|
| eventos_palas | ~113,800 | Evento individual por pala: estado, subtipo, turno, hora inicio/fin, duración, producción y toneladas perdidas |
| resumen_palas | 5,475 | Resumen diario por pala: horas por estado, disponibilidad, producción y pérdida |

Campos principales de `eventos_palas`: `fecha`, `hora_inicio`, `hora_fin`, `pala`,
`estado`, `subtipo`, `turno`, `duracion_hrs`, `produccion_ton`, `toneladas_perdidas`,
`fecha_turno`.

## Lógica de cálculo (KPIs)

```
Disponibilidad %   = Horas Operativas / Horas Totales
Toneladas Perdidas = Suma de toneladas_perdidas (Demora + Malogrado)
Horas Operativas   = Suma de duracion_hrs en estado Operativo
Palas Detenidas    = Número de palas con al menos un evento Malogrado
Budget (ton)       = Horas de detención * tasa de producción del modelo
```

Tasas de producción por modelo: **P&H 4100XPC** ~5,900 ton/h (82 ton/ciclo, 50 s) y
**EX5600-6** ~5,200 ton/h (65 ton/ciclo, 45 s).

## Arquitectura

- **Frontend/back**: aplicación **Dash** (sobre Flask) con callbacks reactivos por
  fecha, pala y tipo de detención.
- **Visualización**: **Plotly** (Graph Objects + Subplots) para el Gantt día/noche.
- **Datos**: Pandas / NumPy; la data se genera con un script de simulación (seed=42).
- **Deploy**: **Render** con `gunicorn`. Endpoint ligero `/health` + monitor externo
  para evitar la suspensión por inactividad (servicio siempre activo).

## Generación de data sintética

Eventos simulados por pala en ciclos de 24 h, particionados en los límites de turno
(08:00 / 20:00). Estados asignados por probabilidad (Operativo 72%, Demora 20%,
Malogrado 8%) y duraciones con distribuciones realistas (normal para Operativo y
Demora, exponencial para Malogrado). La producción y las pérdidas se calculan a partir
de los parámetros de cada modelo de pala.

## Stack tecnológico

| Herramienta | Uso |
|---|---|
| **Python 3.12** | Lenguaje base |
| **Dash** | Framework web del dashboard |
| **Plotly** | Gráficos interactivos (Gantt, subplots) |
| **Pandas / NumPy** | Procesamiento y generación de datos |
| **gunicorn** | Servidor WSGI en producción |
| **Render** | Hosting del demo en vivo |
| **Git / GitHub** | Versionamiento y publicación |

</details>

---

© 2026 Nilson Rolando Garrido Asenjo — Todos los derechos reservados. Ver [LICENSE](LICENSE).
