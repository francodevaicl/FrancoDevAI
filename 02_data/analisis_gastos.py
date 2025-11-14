"""
analisis_gastos.py
Autor: Franco DevAI

Este programa:
1. Lee un archivo CSV de gastos.
2. Calcula el total gastado.
3. Calcula cuánto se gasta por categoría.
4. Calcula promedios por categoría.
5. Calcula porcentajes por categoría.
6. Genera un archivo de resumen de texto listo para entregar.

La idea es que puedas adaptar este análisis a otros archivos
(otros meses, otras personas, pequeñas empresas, etc.).
"""

import csv
from collections import defaultdict


def leer_gastos(ruta_csv):
    """
    Lee un archivo CSV y devuelve una lista de diccionarios.

    Cada fila del CSV se convierte en algo como:
    {"categoria": "comida", "monto": 8500, "detalle": "almuerzo"}

    Parámetros:
        ruta_csv (str): ruta del archivo CSV.

    Retorna:
        list[dict]: lista de gastos.
    """
    gastos = []

    # Abrimos el archivo en modo lectura
    with open(ruta_csv, "r", encoding="utf-8") as archivo:
        # DictReader lee cada fila como un diccionario
        lector = csv.DictReader(archivo)

        for fila in lector:
            # Convertimos el monto de texto a número entero
            fila["monto"] = int(fila["monto"])
            gastos.append(fila)

    return gastos


def total_gastado(gastos):
    """
    Calcula el total gastado sumando todos los montos.

    Parámetros:
        gastos (list[dict]): lista de gastos.

    Retorna:
        int: suma de todos los montos.
    """
    return sum(item["monto"] for item in gastos)


def gastos_por_categoria(gastos):
    """
    Calcula cuánto se gasta en cada categoría.

    Ejemplo de resultado:
        {"comida": 19000, "transporte": 3000, ...}

    Parámetros:
        gastos (list[dict]): lista de gastos.

    Retorna:
        dict[str, int]: diccionario categoría → monto total.
    """
    categorias = defaultdict(int)

    for item in gastos:
        categoria = item["categoria"]
        monto = item["monto"]
        categorias[categoria] += monto

    return categorias


def promedio_por_categoria(gastos):
    """
    Calcula el promedio de gasto por categoría.

    Ejemplo de resultado:
        {"comida": 6333.33, "transporte": 1500.0, ...}

    Aquí primero agrupamos todos los montos de cada categoría en una lista
    y luego calculamos el promedio de cada lista.

    Parámetros:
        gastos (list[dict]): lista de gastos.

    Retorna:
        dict[str, float]: diccionario categoría → promedio.
    """
    montos_por_categoria = defaultdict(list)

    # Recorremos todos los gastos y agrupamos los montos por categoría
    for item in gastos:
        categoria = item["categoria"]
        monto = item["monto"]
        montos_por_categoria[categoria].append(monto)

    # Calculamos el promedio para cada categoría
    promedios = {}
    for categoria, lista_montos in montos_por_categoria.items():
        promedio = sum(lista_montos) / len(lista_montos)
        promedios[categoria] = promedio

    return promedios


def generar_resumen(gastos, ruta_resumen="02_data/resumen_gastos.txt"):
    """
    Genera un archivo de texto con el resumen de los gastos.

    El archivo contiene:
    - Total gastado.
    - Monto y porcentaje por categoría.
    - Promedio de gasto por categoría.

    Parámetros:
        gastos (list[dict]): lista de gastos.
        ruta_resumen (str): ruta donde se guardará el archivo de resumen.
    """
    total = total_gastado(gastos)
    por_categoria = gastos_por_categoria(gastos)
    promedios = promedio_por_categoria(gastos)

    # Abrimos el archivo de salida en modo escritura ("w" sobreescribe)
    with open(ruta_resumen, "w", encoding="utf-8") as f:
        f.write("=== RESUMEN DE GASTOS ===\n")
        f.write(f"Total gastado: {total}\n\n")

        f.write("Por categoría (monto y % del total):\n")
        for categoria, monto in por_categoria.items():
            # Evitamos división por cero
            porcentaje = (monto / total) * 100 if total > 0 else 0
            f.write(f" - {categoria}: {monto} ({porcentaje:.2f}%)\n")

        f.write("\nPromedio por categoría:\n")
        for categoria, prom in promedios.items():
            f.write(f" - {categoria}: {prom:.2f}\n")

    print(f"\nResumen guardado en: {ruta_resumen}")


if __name__ == "__main__":
    """
    Punto de entrada del programa.

    Esta parte se ejecuta SOLO cuando corremos:
        python 02_data/analisis_gastos.py

    Si este archivo se importara desde otro, este bloque no se ejecuta.
    """
    # 1. Definimos la ruta del archivo CSV a analizar
    ruta = "02_data/gastos_demo.csv"

    # 2. Leemos los gastos desde el CSV
    gastos = leer_gastos(ruta)

    # 3. Calculamos el total gastado
    total = total_gastado(gastos)

    print("\n=== ANALISIS DE GASTOS ===")
    print("Total gastado:", total)

    # 4. Mostramos el detalle por categoría con porcentaje
    print("\nPor categoría (monto y % del total):")
    por_cat = gastos_por_categoria(gastos)

    for categoria, monto in por_cat.items():
        porcentaje = (monto / total) * 100 if total > 0 else 0
        print(f" - {categoria}: {monto} ({porcentaje:.2f}%)")

    # 5. Mostramos el promedio por categoría
    print("\nPromedio por categoría:")
    promedios = promedio_por_categoria(gastos)
    for categoria, prom in promedios.items():
        print(f" - {categoria}: {prom:.2f}")

    # 6. Generamos el archivo de resumen para entregar o guardar
    generar_resumen(gastos)
