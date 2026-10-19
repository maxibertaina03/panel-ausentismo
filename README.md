# Panel de control de ausentismo 2024–2025

Tablero web para analizar el ausentismo del personal de planta: ausencias, vacaciones y días de ART por empleado y por mes, con comparación entre 2024 y 2025.

**Autor:** Máximo Bertaina

## Qué muestra

La pantalla tiene filtros en la barra lateral (año, empleado, mes, tipo de ausencia y categoría del motivo) y cinco pestañas:

| Pestaña | Qué tiene |
| --- | --- |
| **Panel de control** | Indicadores generales, los 10 empleados con más días, distribución por tipo y evolución mes a mes. |
| **Análisis individual** | Detalle de un empleado: totales, gráfico mensual y motivos de cada año. |
| **Comparación anual** | 2024 contra 2025, en totales y por mes. |
| **Análisis detallado** | Motivos agrupados por categoría, comparativa mensual y estadísticas descriptivas. |
| **Exportar datos** | Descarga de los datos filtrados, el resumen por empleado y el detalle mensual. |

### Tipos de ausencia

- **Ausente**: faltas, con su motivo.
- **Vacaciones**.
- **ART**: días de licencia por accidente o enfermedad laboral.

Los motivos de las faltas se agrupan solos en categorías: enfermedad, duelo, permiso gremial, cuidado familiar, permiso personal, audiencias o trámites, y sin motivo específico.

## De dónde salen los datos

Los registros están cargados dentro de `app.py`, en la función `load_data()`: una lista para 2024 y otra para 2025. Cada registro tiene empleado, mes, días de ausencia, vacaciones, ART, motivo y total. Para actualizar el tablero hay que editar esas listas.

## Cómo correrlo

Requisitos: Python 3.9 o superior.

```bash
pip install -r requirements.txt
streamlit run app.py
```

El tablero se abre en `http://localhost:8501`.

## Stack

Python, Streamlit, pandas, NumPy y Plotly.
