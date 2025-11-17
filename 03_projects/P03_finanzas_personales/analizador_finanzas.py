import csv
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

"""
P03 - Analizador de finanzas personales (versión 2)

Objetivo:
- Leer un archivo CSV con movimientos de dinero.
- Calcular cuánto se gasta por categoría.
- Calcular promedio diario de gasto.
- Destacar la categoría con más gasto.
- Destacar el gasto individual más alto.
- Mostrar un resumen claro en consola.
- Guardar el mismo resumen en un archivo TXT.
"""

# ==============================
# Rutas de archivos
# ==============================

# carpeta raíz del repo "GIT WORKS FRANCODEVAI"
RUTA_BASE = Path(__file__).resolve().parents[2]

# CSV oficial de este proyecto (en 03_projects)
RUTA_CSV = RUTA_BASE / "03_projects" / "P03_finanzas_personales" / "gastos_demo2.csv"

# TXT de salida con el reporte
RUTA_REPORTE = (
    RUTA_BASE
    / "03_projects"
    / "P03_finanzas_personales"
    / "reporte_gastos_p03.txt"
)


# ==============================
# Modelos de datos
# ==============================

@dataclass
class Movimiento:
    fecha: datetime
    categoria: str
    monto: float
    detalle: str


@dataclass
class ResumenFinanciero:
    fecha_inicio: datetime
    fecha_fin: datetime
    dias_periodo: int
    num_movimientos: int
    total_general: float
    promedio_diario: float
    gasto_por_categoria: Dict[str, float]
    categoria_top: str
    monto_categoria_top: float
    gasto_maximo: Movimiento


# ==============================
# Funciones utilitarias
# ==============================

def formato_clp(monto: float) -> str:
    """Formatea un número como CLP: 12345.6 -> $12.346"""
    return f"${monto:,.0f}".replace(",", ".")


# ==============================
# Lectura y procesamiento de datos
# ==============================

def leer_movimientos(ruta_csv: Path) -> List[Movimiento]:
    """
    Lee un CSV con columnas:
        fecha,categoria,monto,detalle
    y devuelve una lista de Movimiento.
    """
    columnas_requeridas = {"fecha", "categoria", "monto", "detalle"}

    print(f"Leyendo movimientos desde: {ruta_csv}")

    if not ruta_csv.exists():
        raise FileNotFoundError(f"No se encontró el archivo CSV: {ruta_csv}")

    movimientos: List[Movimiento] = []

    with ruta_csv.open(encoding="utf-8") as f:
        lector = csv.DictReader(f)

        if lector.fieldnames is None or not columnas_requeridas.issubset(
            set(lector.fieldnames)
        ):
            raise ValueError(
                f"El CSV debe contener las columnas: {', '.join(columnas_requeridas)}. "
                f"Columnas encontradas: {lector.fieldnames}"
            )

        for fila in lector:
            try:
                fecha = datetime.fromisoformat(fila["fecha"])
            except ValueError:
                print(f"⚠️  Fecha inválida: {fila['fecha']} (se omite fila)")
                continue

            try:
                monto = float(fila["monto"])
            except ValueError:
                print(f"⚠️  Monto inválido: {fila['monto']} (se omite fila)")
                continue

            mov = Movimiento(
                fecha=fecha,
                categoria=fila["categoria"],
                monto=monto,
                detalle=fila["detalle"],
            )
            movimientos.append(mov)

    return movimientos


def calcular_resumen(movimientos: List[Movimiento]) -> ResumenFinanciero:
    """Calcula todos los KPIs financieros a partir de la lista de movimientos."""
    if not movimientos:
        raise ValueError("No hay movimientos para analizar.")

    # Fechas del periodo
    fechas = [m.fecha for m in movimientos]
    fecha_inicio = min(fechas)
    fecha_fin = max(fechas)
    dias_periodo = (fecha_fin - fecha_inicio).days + 1

    # Gasto por categoría
    gasto_por_categoria: Dict[str, float] = defaultdict(float)
    for m in movimientos:
        gasto_por_categoria[m.categoria] += m.monto

    # Total general y promedio diario
    total_general = sum(gasto_por_categoria.values())
    promedio_diario = total_general / dias_periodo

    # Categoría con mayor gasto
    categoria_top, monto_categoria_top = max(
        gasto_por_categoria.items(), key=lambda kv: kv[1]
    )

    # Gasto individual más alto
    gasto_maximo = max(movimientos, key=lambda m: m.monto)

    return ResumenFinanciero(
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        dias_periodo=dias_periodo,
        num_movimientos=len(movimientos),
        total_general=total_general,
        promedio_diario=promedio_diario,
        gasto_por_categoria=dict(gasto_por_categoria),
        categoria_top=categoria_top,
        monto_categoria_top=monto_categoria_top,
        gasto_maximo=gasto_maximo,
    )


# ==============================
# Generación de texto de reporte
# ==============================

def generar_texto_reporte(resumen: ResumenFinanciero) -> str:
    lineas: List[str] = []

    lineas.append("RESUMEN DE GASTOS PERSONALES")
    lineas.append("=" * 60)
    lineas.append(
        f"Período: {resumen.fecha_inicio.date()}  →  {resumen.fecha_fin.date()}"
    )
    lineas.append(f"Días en el período: {resumen.dias_periodo}")
    lineas.append(f"Número de movimientos: {resumen.num_movimientos}")
    lineas.append("-" * 60)

    lineas.append("")
    lineas.append("Gasto por categoría:")
    lineas.append("")

    for categoria, monto in sorted(
        resumen.gasto_por_categoria.items(), key=lambda kv: kv[0]
    ):
        lineas.append(f"  - {categoria:<15} {formato_clp(monto):>12}")

    lineas.append("")
    lineas.append("-" * 60)
    lineas.append(f"TOTAL GENERAL: {formato_clp(resumen.total_general)}")
    lineas.append(
        f"PROMEDIO DIARIO: {formato_clp(resumen.promedio_diario)} "
        f"(en {resumen.dias_periodo} días)"
    )

    lineas.append("")
    lineas.append("Métricas destacadas:")
    lineas.append(
        f"  - Categoría con mayor gasto: {resumen.categoria_top} "
        f"({formato_clp(resumen.monto_categoria_top)})"
    )
    lineas.append(
        "  - Gasto individual más alto: "
        f"{formato_clp(resumen.gasto_maximo.monto)} "
        f"el {resumen.gasto_maximo.fecha.date()} "
        f"({resumen.gasto_maximo.detalle})"
    )

    lineas.append("=" * 60)

    return "\n".join(lineas)


def guardar_reporte(texto: str, ruta: Path) -> None:
    """Guarda el texto en un archivo de reporte."""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(texto, encoding="utf-8")


# ==============================
# Punto de entrada
# ==============================

def main() -> None:
    movimientos = leer_movimientos(RUTA_CSV)
    resumen = calcular_resumen(movimientos)
    texto_reporte = generar_texto_reporte(resumen)

    # Mostrar en consola
    print()
    print(texto_reporte)

    # Guardar en archivo
    guardar_reporte(texto_reporte, RUTA_REPORTE)
    print(f"\nReporte guardado en: {RUTA_REPORTE.resolve()}")


if __name__ == "__main__":
    main()
