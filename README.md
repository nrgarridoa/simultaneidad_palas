# Dashboard de Simultaneidad de Palas

Visualizacion operativa y analitica de palas mineras desarrollada en **Python + Plotly Dash**.

Referencia visual: dashboard de monitoreo de Antamina.

---

## Descripcion General

El **Dashboard de Simultaneidad de Palas** permite analizar, visualizar y comparar el estado operativo de las palas mineras durante los turnos de dia y noche en una operacion minera a cielo abierto.

El proyecto fue construido desde cero en **Python** con **Dash**, simulando datos reales de operacion (data sintetica basada en parametros de palas CAT P&H 4100XPC y EX5600-6).

---

## Funcionalidades Principales

- **Grafico Gantt dividido Dia / Noche** con estados: Operativo, Demora, Malogrado
- **KPIs en tiempo real**: Disponibilidad, Toneladas Perdidas, Horas Operativas, Palas Detenidas
- **Navegacion por fecha** con flechas y filtro por pala
- **Tabla resumen** de palas detenidas con perdida por modelo de equipo
- **Tabla detalle de detenciones** estilo Antamina (Budget, PM, NoPM) con filtro por tipo
- **Exportacion de datos filtrados** a CSV
- **Diseno responsive** estilo industrial minero
- **Despliegue web** en Render Cloud

---

## Contexto Minero

En mineria a cielo abierto, la **simultaneidad de palas** es un indicador clave para evaluar la eficiencia operativa de los equipos de carguio.

Este dashboard simula un monitoreo real de 15 palas (SH001 - SH015) durante todo el anio 2025, registrando su disponibilidad en turnos de **dia (08:00 - 20:00)** y **noche (20:00 - 08:00)**.

Los estados se clasifican en:

- **Operativo** - pala en produccion
- **Demora** - interrupciones menores o logisticas (Espera Camion, Voladura, etc.)
- **Malogrado** - fallas mecanicas: PM (mantenimiento programado) o NoPM (no programado)

---

## Tecnologias Utilizadas

| Categoria           | Tecnologia                          |
|---------------------|-------------------------------------|
| Lenguaje            | Python 3.12                         |
| Framework web       | Dash                                |
| Analisis de datos   | Pandas, NumPy                       |
| Visualizacion       | Plotly (Graph Objects + Subplots)    |
| Estilos             | CSS personalizado (assets/)         |
| Hosting             | Render Cloud                        |
| Control de versiones| Git + GitHub                        |

---

## Estructura del Proyecto

```
simultaneidad_palas/
|
|-- app.py                  # Aplicacion principal Dash
|-- data/
|   |-- eventos_palas.csv   # Data sintetica de eventos
|   |-- resumen_palas.csv   # Resumen diario por pala
|-- scripts/
|   |-- generar_datos.py    # Generador de data sintetica
|-- assets/
|   |-- styles.css          # Estilos del dashboard
|-- requirements.txt        # Dependencias
|-- Procfile                # Configuracion para Render
|-- runtime.txt             # Version de Python
|-- .gitignore
|-- README.md
```

---

## Generacion de Data Sintetica

El dataset se genera automaticamente ejecutando:

```bash
python scripts/generar_datos.py
```

Genera dos archivos en `data/`:
- `eventos_palas.csv` - Eventos individuales con hora inicio/fin, estado, subtipo, duracion, produccion y perdidas
- `resumen_palas.csv` - Resumen diario por pala con horas por estado, disponibilidad y produccion

---

## Ejecucion Local

Clonar el proyecto:

```bash
git clone https://github.com/nrgarridoa/simultaneidad_palas.git
cd simultaneidad_palas
```

Crear entorno virtual:

```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux / Mac
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar:

```bash
python app.py
```

Acceder al dashboard en: `http://127.0.0.1:8050`

---

## Autor

**Nilson R. Garrido Asenjo**
Ingeniero de Minas | Data Analyst | Python Developer

---

## Licencia

Este proyecto se distribuye bajo la licencia MIT.
