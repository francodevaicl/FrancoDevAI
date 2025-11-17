import pandas as pd
from pathlib import Path

"""
P04 - Analizador de redes sociales para artistas/DJs (versión 1)

Objetivo:
- Leer un CSV con publicaciones en redes sociales.
- Ver cuántos posts hay por red y por tipo de contenido.
- Empezar a acostumbrarnos a trabajar con pandas (herramienta clave en data).
"""

# -------------------------------------------------------------------
# 1. Configuración de rutas
# -------------------------------------------------------------------

# Carpeta donde está este archivo .py
BASE_DIR = Path(__file__).resolve().parent

# CSV con los posts de ejemplo
RUTA_CSV = BASE_DIR / "posts_demo.csv"


# -------------------------------------------------------------------
# 2. Funciones principales
# -------------------------------------------------------------------

def cargar_datos(ruta_csv: Path) -> pd.DataFrame:
    """
    Carga el CSV de publicaciones en un DataFrame de pandas.

    Cada fila representa un post, con columnas:
    - fecha
    - red
    - tipo
    - descripcion
    - likes
    - comentarios
    - guardados
    - reproducciones
    """
    if not ruta_csv.exists():
        raise FileNotFoundError(f"No encontré el archivo: {ruta_csv}")

    df = pd.read_csv(ruta_csv)

    # Aseguramos que columnas numéricas sean numéricas
    cols_numericas = ["likes", "comentarios", "guardados", "reproducciones"]
    for col in cols_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


def mostrar_resumen_basico(df: pd.DataFrame) -> None:
    """
    Muestra en consola:
    - primeras filas
    - cantidad de posts por red
    - cantidad de posts por tipo
    """
    print("\n=== Primeras filas del dataset ===")
    print(df.head())

    print("\n=== Número de posts por red ===")
    print(df["red"].value_counts())

    print("\n=== Número de posts por tipo de contenido ===")
    print(df["tipo"].value_counts())


# -------------------------------------------------------------------
# 3. Punto de entrada
# -------------------------------------------------------------------

def main():
    print(f"Leyendo datos desde: {RUTA_CSV}")
    df = cargar_datos(RUTA_CSV)

    print(f"\nTotal de posts cargados: {len(df)}")
    mostrar_resumen_basico(df)


if __name__ == "__main__":
    main()
