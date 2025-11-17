import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path

"""
P03 - Analizador de finanzas personales (versión 2)

Objetivo:
- Leer un archivo CSV con movimientos de dinero.
- Calcular cuánto se gasta por categoría.
- Calcular promedio diario de gasto.
- Mostrar un resumen claro en consola.
- Guardar el mismo resumen en un archivo TXT.
"""


# Rutas de archivos
RUTA_BASE = Path(__file__).resolve().parents[2]  # carpeta GIT WORKS FRANCODEVAI

RUTA_CSV = (
    RUTA_BASE
    / "03_projects"
    / "P03_finanzas_personales"
    / "gastos_demo2.csv"
)

RUTA_REPORTE = (
    RUTA_BASE
    / "03_projects"
    / "P03_finanzas_personales"
    / "reporte_gastos_p03.txt"
)



def leer_movimientos(ruta_csv: Path):
    """
    Lee el archivo CSV de gastos y devuelve una lista de movimientos.

    Cada movimiento es un diccionario con:
    - fecha (datetime.date)
    - categoria (str)
    - monto (int)
    - detalle (str)
    """
    movimientos = []

    columnas_requeridas = {"fecha", "categoria", "monto", "detalle"}

    with ruta_csv.open(encoding="utf-8") as f:
        lector = csv.DictReader(f)

        # Validar columnas
        if not columnas_requeridas.issubset(lector.fieldnames or []):
            raise ValueError(
                f"El archivo CSV debe tener estas columnas: {columnas_requeridas}. "
                f"Columnas encontradas: {lector.fieldnames}"
            )

        for fila in lector:
            try:
                fecha = datetime.strptime(fila["fecha"], "%Y-%m-%d").date()
                categoria = fila["categoria"].strip()
                monto = int(fila["monto"])
                detalle = fila.get("detalle", "").strip()
            except Exception as e:
                print(f"[ADVERTENCIA] No se pudo leer la fila {fila}: {e}")
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


def calcular_estadisticas(movimientos):
    """
    A partir de la lista de movimientos, calcula:

    - gasto_por_categoria: dict[cat] = total
    - total_general: int
    - fecha_min, fecha_max: datetime.date
    - num_movimientos: int
    - num_dias: int
    - promedio_diario: float
    """
    if not movimientos:
        raise ValueError("No hay movimientos para analizar.")

    gasto_por_categoria = defaultdict(int)
    fechas = []
    total_general = 0

    for mov in movimientos:
        categoria = mov["categoria"]
        monto = mov["monto"]
        fecha = mov["fecha"]

        gasto_por_categoria[categoria] += monto
        total_general += monto
        fechas.append(fecha)

    fecha_min = min(fechas)
    fecha_max = max(fechas)
    num_movimientos = len(movimientos)

    # Número de días (incluyendo ambos extremos)
    num_dias = (fecha_max - fecha_min).days + 1
    promedio_diario = total_general / num_dias if num_dias > 0 else 0

    return {
        "gasto_por_categoria": dict(gasto_por_categoria),
        "total_general": total_general,
        "fecha_min": fecha_min,
        "fecha_max": fecha_max,
        "num_movimientos": num_movimientos,
        "num_dias": num_dias,
        "promedio_diario": promedio_diario,
    }


def formatear_monto(monto: int) -> str:
    """
    Devuelve el monto en formato $XX.XXX usando puntos como separador de miles.
    """
    return "$" + f"{monto:,.0f}".replace(",", ".")


def generar_reporte_texto(estadisticas: dict) -> str:
    """
    Genera el texto del reporte a partir del diccionario de estadísticas.
    Ahora incluye:
    - porcentaje de gasto por categoría
    - categoría con mayor gasto
    """
    gasto_por_categoria = estadisticas["gasto_por_categoria"]
    total_general = estadisticas["total_general"]
    fecha_min = estadisticas["fecha_min"]
    fecha_max = estadisticas["fecha_max"]
    num_movimientos = estadisticas["num_movimientos"]
    num_dias = estadisticas["num_dias"]
    promedio_diario = estadisticas["promedio_diario"]

    # Porcentaje por categoría
    porcentaje_por_categoria = {
        cat: (monto / total_general * 100) if total_general else 0
        for cat, monto in gasto_por_categoria.items()
    }

    # Categoría con mayor gasto
    categoria_top = None
    monto_top = 0
    if gasto_por_categoria:
        categoria_top, monto_top = max(
            gasto_por_categoria.items(), key=lambda x: x[1]
        )

    lineas = []
    lineas.append("RESUMEN DE GASTOS PERSONALES")
    lineas.append("=" * 60)
    lineas.append(
        f"Período: {fecha_min.isoformat()}  ->  {fecha_max.isoformat()}"
    )
    lineas.append(f"Número de movimientos: {num_movimientos}")
    lineas.append(f"Número de días:        {num_dias}")
    lineas.append("")

    # Gasto por categoría con porcentajes
    lineas.append("Gasto por categoría:")
    lineas.append("")

    if gasto_por_categoria:
        ancho_cat = max(len(cat) for cat in gasto_por_categoria)
        for categoria, monto in sorted(
            gasto_por_categoria.items(), key=lambda x: x[0]
        ):
            porcentaje = porcentaje_por_categoria.get(categoria, 0.0)
            linea = (
                f"  - {categoria:<{ancho_cat}}  "
                f"{formatear_monto(monto):>12}   "
                f"({porcentaje:5.1f} %)"
            )
            lineas.append(linea)
    else:
        lineas.append("  (sin datos)")

    lineas.append("")
    lineas.append("-" * 60)
    lineas.append(f"TOTAL GENERAL:       {formatear_monto(total_general)}")
    lineas.append(
        f"PROMEDIO DIARIO:     {formatear_monto(round(promedio_diario))}"
    )

    # Info de categoría con mayor gasto
    if categoria_top is not None:
        porcentaje_top = porcentaje_por_categoria.get(categoria_top, 0.0)
        lineas.append("")
        lineas.append("Categoría con mayor gasto:")
        lineas.append(
            f"  > {categoria_top}  ->  {formatear_monto(monto_top)} "
            f"({porcentaje_top:5.1f} % del total)"
        )

    lineas.append("")
    lineas.append("=" * 60)

    return "\n".join(lineas)


def guardar_reporte(texto: str, ruta_reporte: Path) -> None:
    """
    Guarda el reporte en un archivo de texto.
    """
    ruta_reporte.parent.mkdir(parents=True, exist_ok=True)
    with ruta_reporte.open("w", encoding="utf-8") as f:
        f.write(texto)


def main():
    print("Leyendo movimientos desde:", RUTA_CSV)
    movimientos = leer_movimientos(RUTA_CSV)

    print(f"Movimientos cargados: {len(movimientos)}")

    estadisticas = calcular_estadisticas(movimientos)
    reporte = generar_reporte_texto(estadisticas)

    # Mostrar en consola
    print()
    print(reporte)

    # Guardar en archivo
    guardar_reporte(reporte, RUTA_REPORTE)
    print(f"\nReporte guardado en: {RUTA_REPORTE.resolve()}")


if __name__ == "__main__":
    main()
