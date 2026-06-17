# Dashboard de Simultaneidad de Palas

> Visualizacion operativa y analitica de palas mineras — Python + Plotly Dash.

[![Demo en vivo](https://img.shields.io/badge/Demo-en%20vivo-2ea44f?style=for-the-badge)](https://simultaneidad-palas.onrender.com)
&nbsp;
![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python&logoColor=white)
![Dash](https://img.shields.io/badge/Dash-Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-NumPy-150458?style=flat-square&logo=pandas&logoColor=white)

🔗 **Demo en vivo:** https://simultaneidad-palas.onrender.com

---

## 📊 Descripcion

El **Dashboard de Simultaneidad de Palas** permite analizar, visualizar y comparar
el estado operativo de palas mineras durante los turnos de dia y noche en una
operacion a cielo abierto. Construido desde cero en **Python** con **Dash / Plotly**,
sobre data sintetica basada en parametros reales de palas CAT P&H 4100XPC y EX5600-6.

En mineria a cielo abierto, la **simultaneidad de palas** es un indicador clave de la
eficiencia operativa del carguio: cuantos equipos estan produciendo al mismo tiempo
frente a los que estan detenidos.

---

## ✨ Funcionalidades

- **Gantt dia / noche** con estados Operativo, Demora y Malogrado por equipo.
- **KPIs en tiempo real**: disponibilidad, toneladas perdidas, horas operativas y palas detenidas.
- **Navegacion por fecha** y **filtro por pala**.
- **Tabla resumen** de detenciones con perdida por modelo de equipo.
- **Tabla detalle** (Budget, PM, NoPM) con filtro por tipo de detencion.
- **Exportacion a CSV** de los datos filtrados.
- **Diseno responsive** de estilo industrial minero.

---

## 📸 Vista previa

_(Captura del dashboard)_

<!-- Para mostrar la captura: agrega el archivo docs/preview.png y descomenta la linea siguiente -->
<!-- ![Vista previa del dashboard](docs/preview.png) -->

---

## 🛠️ Stack tecnologico

| Categoria          | Tecnologia                        |
|--------------------|-----------------------------------|
| Lenguaje           | Python 3.12                       |
| Framework web      | Dash                              |
| Analisis de datos  | Pandas, NumPy                     |
| Visualizacion      | Plotly (Graph Objects + Subplots) |
| Hosting            | Render Cloud                      |

---

## 👤 Autor

**Nilson Rolando Garrido Asenjo**
Mining Engineer | Data Analyst | Python Developer
🌐 [nrgarridoa.github.io](https://nrgarridoa.github.io)

---

## 📄 Codigo y licencia

El **codigo fuente de esta aplicacion es privado**. Esta vitrina presenta el proyecto
y su demo en vivo; el codigo esta disponible para revision **bajo solicitud**.

© 2026 Nilson Rolando Garrido Asenjo — Todos los derechos reservados. Ver [LICENSE](LICENSE).
