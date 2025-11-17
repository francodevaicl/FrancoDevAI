import csv
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. Función: Leer CSV (reutiliza tu P01 pero más compacta)
# ---------------------------------------------------------
def leer_gastos(ruta_csv):
    gastos = []

    with open(ruta_csv, "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            fila["monto"] = int(fila["monto"])
            gastos.append(fila)

    return gastos


# ---------------------------------------------------------
# 2. Función: Calcular métricas principales
# ---------------------------------------------------------
def calcular_metricas(gastos):
    total = sum(g["monto"] for g in gastos)
    promedio = total / len(gastos) if gastos else 0

    # Agrupar por categoría
    categorias = {}
    for g in gastos:
        cat = g["categoria"]
        categorias[cat] = categorias.get(cat, 0) + g["monto"]

    # Ranking categorías
    categorias_ordenadas = sorted(categorias.items(), key=lambda x: x[1], reverse=True)

    # Top 3
    top3 = categorias_ordenadas[:3]

    # Gasto máximo individual
    gasto_max = max(gastos, key=lambda x: x["monto"])

    return total, promedio, categorias, top3, gasto_max


# ---------------------------------------------------------
# 3. Función: Generar gráfico
# ---------------------------------------------------------
def generar_grafico(categorias):
    nombres = list(categorias.keys())
    montos = list(categorias.values())

    plt.figure(figsize=(8, 5))
    plt.bar(nombres, montos)
    plt.title("Gasto por Categoría")
    plt.xlabel("Categorías")
    plt.ylabel("Monto gastado")
    plt.tight_layout()
    plt.savefig("02_data/grafico_gastos.png")
    plt.close()


# ---------------------------------------------------------
# 4. Función: Guardar reporte en archivo TXT
# ---------------------------------------------------------
def guardar_reporte(total, promedio, categorias, top3, gasto_max):
    with open("02_data/reporte_gastos.txt", "w", encoding="utf-8") as archivo:
        archivo.write("=== REPORTE FINANCIERO ===\n\n")
        archivo.write(f"Total gastado: ${total}\n")
        archivo.write(f"Promedio por gasto: ${promedio:.2f}\n\n")

        archivo.write("Gasto por categoría:\n")
        for c, m in categorias.items():
            archivo.write(f" - {c}: ${m}\n")

        archivo.write("\nTop 3 categorías:\n")
        for c, m in top3:
            archivo.write(f" - {c}: ${m}\n")

        archivo.write("\nGasto individual más alto:\n")
        archivo.write(f" - {gasto_max['categoria']}: ${gasto_max['monto']} ({gasto_max['detalle']})\n")


# ---------------------------------------------------------
# 5. PROGRAMA PRINCIPAL
# ---------------------------------------------------------
if __name__ == "__main__":
    ruta = "02_data/gastos_demo.csv"

    gastos = leer_gastos(ruta)

    if not gastos:
        print("Error: No se pudieron leer los gastos.")
        exit()

    total, promedio, categorias, top3, gasto_max = calcular_metricas(gastos)

    generar_grafico(categorias)
    guardar_reporte(total, promedio, categorias, top3, gasto_max)

    print("Dashboard generado correctamente:")
    print(" - grafico_gastos.png creado")
    print(" - reporte_gastos.txt creado")
