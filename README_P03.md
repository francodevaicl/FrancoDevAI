# P03 – Analizador de Finanzas Personales

**Objetivo:**  
Construir una herramienta simple, en Python, para analizar movimientos de dinero desde un archivo CSV y obtener un resumen financiero claro, útil y rápido de leer.

Este proyecto forma parte de mi portafolio de automatización y análisis de datos en Python.

---

## 1. Qué hace este proyecto

A partir del archivo `gastos_demo2.csv`, el programa:

1. Lee todos los movimientos de gasto.
2. Calcula:
   - Gasto total del período.
   - Gasto por categoría.
   - Número de movimientos.
   - Duración del período (en días).
   - Promedio diario de gasto.
3. Destaca métricas clave:
   - **Categoría con mayor gasto**.
   - **Gasto individual más alto** (monto, fecha y detalle).
4. Muestra el resumen en la consola.
5. Guarda el mismo resumen en un archivo de reporte TXT.

---

## 2. Estructura relevante del proyecto

```text
GIT WORKS FRANCODEVAI/
├─ 02_data/
│   └─ ... (otros proyectos)
└─ 03_projects/
    └─ P03_finanzas_personales/
        ├─ analizador_finanzas.py      # Script principal
        ├─ gastos_demo2.csv            # Datos de ejemplo (movimientos)
        └─ reporte_gastos_p03.txt      # Reporte generado
