import csv
from collections import defaultdict

# Leer archivo CSV
def leer_gastos(ruta_csv):
    gastos = []
    with open(ruta_csv, "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            fila["monto"] = int(fila["monto"])  # convertir a número
            gastos.append(fila)
    return gastos

# Total gastado
def total_gastado(gastos):
    return sum(item["monto"] for item in gastos)

# Gastos por categoría
def gastos_por_categoria(gastos):
    categorias = defaultdict(int)
    for item in gastos:
        categorias[item["categoria"]] += item["monto"]
    return categorias

# Promedio por categoría
def promedio_por_categoria(gastos):
    contador = defaultdict(list)
    for item in gastos:
        contador[item["categoria"]].append(item["monto"])

    promedios = {cat: sum(vals)/len(vals) for cat, vals in contador.items()}
    return promedios

if __name__ == "__main__":
    ruta = "02_data/gastos_demo.csv"
    gastos = leer_gastos(ruta)

    total = total_gastado(gastos)

    print("\n=== ANALISIS DE GASTOS ===")
    print("Total gastado:", total)

    # -------- NUEVO BLOQUE CON PORCENTAJES --------
    print("\nPor categoría (monto y % del total):")
    por_cat = gastos_por_categoria(gastos)

    for cat, monto in por_cat.items():
        porcentaje = (monto / total) * 100
        print(f" - {cat}: {monto} ({porcentaje:.2f}%)")
    # ------------------------------------------------

    print("\nPromedio por categoría:")
    for cat, prom in promedio_por_categoria(gastos).items():
        print(f" - {cat}: {prom:.2f}")

    print("\nPromedio por categoría:")
    for cat, prom in promedio_por_categoria(gastos).items():
        print(f" - {cat}: {prom:.2f}")
