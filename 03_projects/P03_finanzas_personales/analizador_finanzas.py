import csv
from collections import defaultdict
from pathlib import Path

"""
P03 - Analizador de finanzas personales (versión 1)

Objetivo:
- Leer un archivo CSV con movimientos de dinero.
- Calcular cuánto se gasta por categoría.
- Mostrar un resumen claro en consola.

Archivo de datos esperado:
- Nombre: gastos_demo2.csv
- Ubicación: misma carpeta que este archivo .py
- Formato CSV (cabecera obligatoria):
    fecha,categoria,monto,detalle
"""

# ---------------------------------------------------------------------------
# Configuración general
# ---------------------------------------------------------------------------

# Carpeta donde está este archivo .py
BASE_DIR = Path(__file__).resolve().parent

# Ruta del CSV oficial de este proyecto
RUTA_CSV = BASE_DIR / "gastos_demo2.csv"

# Columnas que deben existir en el CSV
COLUMNAS_REQUERIDAS = {"fecha", "categoria", "monto", "detalle"}


# ---------------------------------------------------------------------------
# Funciones de utilidad
# ---------------------------------------------------------------------------

def leer_movimientos(ruta_csv: Path):
    """
    Lee el CSV y devuelve una lista de diccionarios (uno por movimiento).

    Cada diccionario tiene las claves:
    - "fecha"
    - "categoria"
    - "monto"
    - "detalle"

    Si el archivo está vacío, no tiene cabecera o le faltan columnas,
    lanza un ValueError con un mensaje claro.
    """
    if not ruta_csv.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_csv}")

    with ruta_csv.open(mode="r", newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        # 1) Verificar que el archivo tenga cabecera
        if lector.fieldnames is None:
            raise ValueError(
                f"El archivo {ruta_csv} está vacío o no tiene fila de cabecera.\n"
                f"Se esperaba algo como: fecha,categoria,monto,detalle"
            )

        columnas_en_archivo = set(lector.fieldnames)

        # 2) Verificar que estén todas las columnas obligatorias
        faltantes = COLUMNAS_REQUERIDAS - columnas_en_archivo
        if faltantes:
            raise ValueError(
                f"Al archivo {ruta_csv.name} le faltan estas columnas: {faltantes}\n"
                f"Columnas encontradas: {columnas_en_archivo}\n"
                f"Cabecera esperada: {COLUMNAS_REQUERIDAS}"
            )

        # 3) Cargar todos los movimientos en memoria
        movimientos = list(lector)
        if not movimientos:
            raise ValueError(
                f"El archivo {ruta_csv.name} solo tiene la cabecera, "
                f"pero no contiene movimientos."
            )

        return movimientos


def calcular_gasto_por_categoria(movimientos):
    """
    Recibe una lista de movimientos (dicts) y devuelve un dict:

        { categoria_normalizada: total_gastado }

    - Convierte el monto a float.
    - Ignora filas cuyo monto no se pueda interpretar.
    - Normaliza la categoría a minúsculas y sin espacios iniciales/finales.
    """
    totales = defaultdict(float)

    for mov in movimientos:
        categoria = (mov.get("categoria") or "").strip().lower()
        monto_bruto = (mov.get("monto") or "").strip()

        if not categoria:
            # Si no hay categoría, ignoramos la fila
            print(f"[AVISO] Fila sin categoría, se ignora: {mov}")
            continue

        try:
            # Permitimos montos como "1000", "1.000", "1,000.50", etc.
            monto_limpio = monto_bruto.replace(".", "").replace(",", ".")
            monto = float(monto_limpio)
        except ValueError:
            print(
                f"[AVISO] No se pudo interpretar el monto '{monto_bruto}' "
                f"en la categoría '{categoria}'. Fila ignorada."
            )
            continue

        totales[categoria] += monto

    return dict(totales)


def obtener_rango_fechas(movimientos):
    """
    A partir de la lista de movimientos, devuelve (fecha_min, fecha_max)
    en formato string, o (None, None) si no se pudieron leer.
    """
    fechas = [
        (mov.get("fecha") or "").strip()
        for mov in movimientos
        if (mov.get("fecha") or "").strip()
    ]

    if not fechas:
        return None, None

    fechas_ordenadas = sorted(fechas)
    return fechas_ordenadas[0], fechas_ordenadas[-1]


def formatear_monto(monto):
    """
    Devuelve el monto formateado estilo CL/ES:
    10000 -> $10.000
    """
    return "$" + f"{monto:,.0f}".replace(",", ".")


def mostrar_resumen(movimientos, totales_por_categoria):
    """
    Imprime en consola un resumen legible:
    - rango de fechas
    - número de movimientos
    - tabla de gasto por categoría
    - total general
    """
    print("\n" + "=" * 70)
    print("RESUMEN DE GASTOS PERSONALES")
    print("=" * 70)

    fecha_min, fecha_max = obtener_rango_fechas(movimientos)
    if fecha_min and fecha_max:
        print(f"Período: {fecha_min}  →  {fecha_max}")
    print(f"Número de movimientos: {len(movimientos)}\n")

    if not totales_por_categoria:
        print("No se encontraron gastos válidos para mostrar.")
        return

    print("Gasto por categoría:\n")

    total_general = 0.0

    # Ordenamos categorías de mayor a menor gasto
    for categoria, total in sorted(
        totales_por_categoria.items(), key=lambda x: x[1], reverse=True
    ):
        print(f"  - {categoria:<20} {formatear_monto(total)}")
        total_general += total

    print("\n" + "-" * 70)
    print(f"TOTAL GENERAL: {formatear_monto(total_general)}")
    print("-" * 70 + "\n")


# ---------------------------------------------------------------------------
# Punto de entrada principal
# ---------------------------------------------------------------------------

def main():
    print(f"Leyendo datos desde: {RUTA_CSV}\n")

    try:
        movimientos = leer_movimientos(RUTA_CSV)
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        return
    except ValueError as e:
        print(f"[ERROR] {e}")
        return

    totales_por_categoria = calcular_gasto_por_categoria(movimientos)
    mostrar_resumen(movimientos, totales_por_categoria)


if __name__ == "__main__":
    main()
