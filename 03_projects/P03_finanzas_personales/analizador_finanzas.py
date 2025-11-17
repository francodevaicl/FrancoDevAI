import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------
# Configuración de rutas
# ---------------------------------------------------------

# CSV con tus gastos (en la misma carpeta que este script)
RUTA_CSV = Path("gastos_demo2.csv")

# Archivo donde se guardará el reporte de texto
RUTA_REPORTE = Path("reporte_gastos_p03.txt")

# Columnas que el CSV debe tener sí o sí
COLUMNAS_REQUERIDAS = {"fecha", "categoria", "monto", "detalle"}


# ---------------------------------------------------------
# Lectura de datos
# ---------------------------------------------------------

def leer_movimientos(ruta_csv: Path):
    """
    Lee los movimientos desde un archivo CSV y devuelve una lista de dicts.

    Cada movimiento tiene:
    {
        "fecha": date,
        "categoria": str,
        "monto": int,
        "detalle": str
    }
    """
    if not ruta_csv.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_csv}")

    movimientos = []

    with ruta_csv.open(encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        if lector.fieldnames is None:
            raise ValueError("El archivo CSV está vacío.")

        # Normalizamos los nombres de las columnas
        columnas_archivo = {nombre.strip().lower() for nombre in lector.fieldnames}

        if not COLUMNAS_REQUERIDAS.issubset(columnas_archivo):
            raise ValueError(
                f"El CSV debe contener las columnas: {COLUMNAS_REQUERIDAS}, "
                f"pero tiene: {columnas_archivo}"
            )

        for fila in lector:
            try:
                fecha = datetime.strptime(fila["fecha"], "%Y-%m-%d").date()
                categoria = fila["categoria"].strip().lower()
                monto = int(fila["monto"])
                detalle = fila.get("detalle", "").strip()
            except (KeyError, ValueError):
                # Si hay una fila mal escrita, la saltamos sin romper el programa
                continue

            movimientos.append(
                {
                    "fecha": fecha,
                    "categoria": categoria,
                    "monto": monto,
                    "detalle": detalle,
                }
            )

    return movimientos


# ---------------------------------------------------------
# Cálculos
# ---------------------------------------------------------

def calcular_resumen(movimientos):
    """
    Recibe una lista de movimientos y calcula:
    - rango de fechas
    - número de movimientos
    - gasto por categoría
    - total general
    - promedio diario
    - categoría con mayor gasto
    - movimiento individual más grande
    """
    if not movimientos:
        raise ValueError("La lista de movimientos está vacía.")

    gasto_por_categoria = defaultdict(int)
    fechas = []
    total_general = 0
    movimiento_mayor = None  # dict con el movimiento de mayor monto

    for mov in movimientos:
        fechas.append(mov["fecha"])
        gasto_por_categoria[mov["categoria"]] += mov["monto"]
        total_general += mov["monto"]

        if movimiento_mayor is None or mov["monto"] > movimiento_mayor["monto"]:
            movimiento_mayor = mov

    fecha_min = min(fechas)
    fecha_max = max(fechas)
    num_movimientos = len(movimientos)

    # Número de días en el período (incluyendo ambos extremos)
    dias_periodo = (fecha_max - fecha_min).days + 1
    promedio_diario = total_general / dias_periodo if dias_periodo > 0 else 0

    # Categoría con mayor gasto
    categoria_top = max(
        gasto_por_categoria.items(), key=lambda par: par[1]
    ) if gasto_por_categoria else (None, 0)

    resumen = {
        "fecha_min": fecha_min,
        "fecha_max": fecha_max,
        "num_movimientos": num_movimientos,
        "gasto_por_categoria": gasto_por_categoria,
        "total_general": total_general,
        "promedio_diario": promedio_diario,
        "categoria_top": categoria_top,
        "movimiento_mayor": movimiento_mayor,
    }

    return resumen


# ---------------------------------------------------------
# Formateo e impresión
# ---------------------------------------------------------

def formatear_resumen(resumen):
    """
    Recibe el dict de resumen y devuelve un texto listo para imprimir / guardar.
    """
    lineas = []

    lineas.append("RESUMEN DE GASTOS PERSONALES")
    lineas.append("=" * 60)
    lineas.append(
        f"Período: {resumen['fecha_min']}  →  {resumen['fecha_max']}"
    )
    lineas.append(f"Número de movimientos: {resumen['num_movimientos']}")
    lineas.append("")

    lineas.append("Gasto por categoría:")
    lineas.append("")

    for categoria, monto in sorted(
        resumen["gasto_por_categoria"].items(), key=lambda par: par[0]
    ):
        lineas.append(f"  - {categoria:15} ${monto:,.0f}".replace(",", "."))

    lineas.append("-" * 60)
    lineas.append(
        f"TOTAL GENERAL:           ${resumen['total_general']:,.0f}".replace(",", ".")
    )
    lineas.append(
        f"PROMEDIO DIARIO:         ${resumen['promedio_diario']:,.0f}".replace(",", ".")
    )
    lineas.append("")

    categoria_top, monto_top = resumen["categoria_top"]
    if categoria_top is not None:
        lineas.append(
            f"Categoría con mayor gasto: {categoria_top} "
            f"(${monto_top:,.0f})".replace(",", ".")
        )

    mov_max = resumen["movimiento_mayor"]
    if mov_max:
        lineas.append(
            "Movimiento individual más grande: "
            f"{mov_max['fecha']} | {mov_max['categoria']} | "
            f"${mov_max['monto']:,.0f} | {mov_max['detalle']}".replace(",", ".")
        )

    lineas.append("=" * 60)

    return "\n".join(lineas)


def guardar_reporte(texto, ruta_salida: Path):
    """
    Guarda el resumen en un archivo de texto.
    """
    with ruta_salida.open("w", encoding="utf-8") as archivo:
        archivo.write(texto)


# ---------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------

def main():
    try:
        movimientos = leer_movimientos(RUTA_CSV)
    except Exception as e:
        print(f"[ERROR] No fue posible leer el archivo CSV: {e}")
        return

    if not movimientos:
        print("No se encontraron movimientos válidos.")
        return

    resumen = calcular_resumen(movimientos)
    texto_resumen = formatear_resumen(resumen)

    # Mostrar en consola
    print(texto_resumen)

    # Guardar en archivo
    guardar_reporte(texto_resumen, RUTA_REPORTE)
    print(f"\nReporte guardado en: {RUTA_REPORTE.resolve()}")


if __name__ == "__main__":
    main()
