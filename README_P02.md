📊 P02 — Dashboard de Finanzas Personales (v0.2)

Este proyecto genera un informe automático de gastos a partir de un archivo CSV.
Produce:

Totales generales

Totales por categoría

Porcentajes de gasto

Promedios

Gráfico circular (grafico_gastos.png)

Reporte en texto (reporte_gastos.txt)

Todo usando Python, sin necesidad de conocimientos avanzados por parte del usuario.

🚀 Objetivo del Proyecto

El objetivo es crear una herramienta simple pero poderosa para:

visualizar gastos personales,

detectar patrones,

mejorar la planificación financiera,

y automatizar tareas repetitivas.

Este proyecto combina procesamiento de datos, análisis básico y visualización.
Es tu primera herramienta real de análisis financiero automatizado.

📂 Estructura del Proyecto
02_data/
│
├── P02_dashboard.py        # Script principal
├── analisis_gastos.py      # Funciones del proyecto P01
├── gastos_demo.csv         # Dataset de ejemplo
├── grafico_gastos.png      # Gráfico generado automáticamente
└── reporte_gastos.txt      # Informe final generado

📥 Entrada (Dataset)

El script usa como fuente:

02_data/gastos_demo.csv


Formato esperado del CSV:

categoria	monto	detalle
comida	8000	almuerzo
servicios	60000	electricidad
transporte	2000	bus
📤 Salidas Generadas
1️⃣ 📄 reporte_gastos.txt

Incluye:

total gastado

gastos por categoría

porcentajes

top 3 categorías

gasto más alto

2️⃣ 📊 grafico_gastos.png

Muestra los gastos por categoría en una visualización simple.

🧠 Tecnologías utilizadas

Python 3.x

Módulo CSV

Matplotlib

Manipulación de listas y diccionarios

Escritura de archivos

▶️ Cómo ejecutar

Desde la raíz del proyecto:

python 02_data/P02_dashboard.py


Asegúrate de tener instalado matplotlib:

python -m pip install matplotlib

🔮 Futuras mejoras (v0.3, v0.4)

Exportar reporte a PDF

Dashboard web con Streamlit

Conexión con Google Sheets

Alertas automáticas si se supera un límite de gasto

👤 Autor

Franco DevAI
Proyecto práctico orientado a desarrollo profesional en automatización y análisis de datos.