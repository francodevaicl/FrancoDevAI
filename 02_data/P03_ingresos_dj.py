import csv
from collections import defaultdict

"""
P03 – Analizador de Ingresos DJ (v0.1)
Autor: Franco DevAI

Objetivo:
- Leer eventos DJ desde un CSV.
- Calcular:
    * ingreso total
    * ingreso neto (después de costos)
    * ingreso por tipo de evento
    * ingreso por lugar
    * valor hora promedio
- Generar un pequeño reporte en texto.

Más adelante (v0.2+):
- Gráficos
- Filtros por mes
- Promedios móviles
"""


def leer_eventos(ruta_csv):
    """Lee el archivo CSV de eventos DJ y devuelve una lista de diccionarios."""
    eventos = []

    with open(ruta_csv, "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            # Convertimos los campos numéricos a int
            fila["horas"] = int(fila["horas"])
            fila["pago_base"] = int(fila["pago_base"])
            fila["propina"] = int(fila["propina"])
            fila["transporte"] = int(fila["transporte"])
            fila["otros_costos"] = int(fila["otros_costos"])
            eventos.append(fila)

    return eventos


def calcular_metricas_basicas(eventos):
    """
    A partir de la lista de eventos, calcula:
    - ingreso total bruto
    - ingreso total neto (descontando costos)
    - valor hora promedio
    """
    if not eventos:
        return 0, 0, 0

    ingreso_total_bruto = 0
    ingreso_total_neto = 0
    horas_totales = 0

    for e in eventos:
        ingreso_bruto = e["pago_base"] + e["propina"]
        costos = e["transporte"] + e["otros_costos"]
        ingreso_neto = ingreso_bruto - costos

        ingreso_total_bruto += ingreso_bruto
        ingreso_total_neto += ingreso_neto
        horas_totales += e["horas"]

    valor_hora_promedio = ingreso_total_neto / horas_totales if horas_totales > 0 else 0

    return ingreso_total_bruto, ingreso_total_neto, valor_hora_promedio


def generar_reporte(eventos, ruta_reporte="02_data/reporte_ingresos_dj.txt"):
    """
    Genera un archivo de texto con un resumen simple de los ingresos.
    """
    ingreso_bruto, ingreso_neto, valor_hora = calcular_metricas_basicas(eventos)

    with open(ruta_reporte, "w", encoding="utf-8") as f:
        f.write("=== REPORTE DE INGRESOS DJ ===\n\n")
        f.write(f"Ingreso total bruto: ${ingreso_bruto}\n")
        f.write(f"Ingreso total neto:  ${ingreso_neto}\n")
        f.write(f"Valor hora promedio: ${valor_hora:.2f}\n")

    print(f"Reporte generado en: {ruta_reporte}")


if __name__ == "__main__":
    ruta = "02_data/eventos_dj_demo.csv"
    eventos = leer_eventos(ruta)

    if not eventos:
        print("No se encontraron eventos.")
    else:
        generar_reporte(eventos)
