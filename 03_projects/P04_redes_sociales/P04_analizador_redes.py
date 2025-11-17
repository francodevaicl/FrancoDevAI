import pandas as pd
from pathlib import Path

"""
P04 - Analizador de redes sociales para artistas/DJs (versión 2)

Objetivo:
- Leer un CSV con publicaciones en redes sociales.
- Ver cuántos posts hay por red y por tipo.
- Calcular una métrica simple de "engagement" por post.
- Detectar:
    * la red con mayor engagement promedio
    * el tipo de contenido con mayor engagement promedio
    * el post con mayor engagement
- Mostrar un resumen en consola.
- Guardar el resumen en un archivo de texto.
"""

# -------------------------------------------------------------------
# 1. Configuración de rutas
# -------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

RUTA_CSV = BASE_DIR / "posts_demo.csv"
RUTA_REPORTE = BASE_DIR / "reporte_redes.txt"


# -------------------------------------------------------------------
# 2. Carga y preparación de datos
# -------------------------------------------------------------------

def cargar_datos(ruta_csv: Path) -> pd.DataFrame:
    """
    Carga el CSV de publicaciones en un DataFrame de pandas y
    asegura que las columnas numéricas sean numéricas.
    """
    if not ruta_csv.exists():
        raise FileNotFoundError(f"No encontré el archivo: {ruta_csv}")

    df = pd.read_csv(ruta_csv)

    # Aseguramos que columnas numéricas sean numéricas
    cols_numericas = ["likes", "comentarios", "guardados", "reproducciones"]
    for col in cols_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Creamos una columna de engagement simple:
    # likes + comentarios + guardados
    df["engagement"] = df["likes"] + df["comentarios"] + df["guardados"]

    return df


# -------------------------------------------------------------------
# 3. Resúmenes y métricas
# -------------------------------------------------------------------

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


def calcular_metricas_engagement(df: pd.DataFrame) -> dict:
    """
    Calcula métricas de engagement y las devuelve en un diccionario.
    """
    total_posts = len(df)
    engagement_promedio = df["engagement"].mean()

    # Engagement promedio por red
    eng_por_red = df.groupby("red")["engagement"].mean().sort_values(ascending=False)

    # Engagement promedio por tipo de contenido
    eng_por_tipo = df.groupby("tipo")["engagement"].mean().sort_values(ascending=False)

    # Post con mayor engagement
    post_top = df.sort_values("engagement", ascending=False).iloc[0]

    return {
        "total_posts": total_posts,
        "engagement_promedio": engagement_promedio,
        "eng_por_red": eng_por_red,
        "eng_por_tipo": eng_por_tipo,
        "post_top": post_top,
    }


def mostrar_metricas_engagement(metricas: dict) -> None:
    """
    Imprime en consola las métricas de engagement.
    """
    print("\n=== Métricas de engagement ===")
    print(f"Total de posts: {metricas['total_posts']}")
    print(f"Engagement promedio por post: {metricas['engagement_promedio']:.2f}")

    print("\n--- Engagement promedio por red ---")
    print(metricas["eng_por_red"])

    print("\n--- Engagement promedio por tipo de contenido ---")
    print(metricas["eng_por_tipo"])

    post_top = metricas["post_top"]
    print("\n--- Post con mayor engagement ---")
    print(
        f"Fecha: {post_top['fecha']}\n"
        f"Red: {post_top['red']}\n"
        f"Tipo: {post_top['tipo']}\n"
        f"Descripción: {post_top['descripcion']}\n"
        f"Likes: {post_top['likes']}, Comentarios: {post_top['comentarios']}, "
        f"Guardados: {post_top['guardados']}\n"
        f"Engagement total: {post_top['engagement']}"
    )


# -------------------------------------------------------------------
# 4. Generación de reporte en texto
# -------------------------------------------------------------------

def generar_reporte_texto(df: pd.DataFrame, metricas: dict) -> str:
    """
    Genera un texto con el resumen y las métricas de engagement.
    """
    lineas = []

    lineas.append("REPORTE DE REDES SOCIALES (P04)")
    lineas.append("=" * 60)
    lineas.append(f"Total de posts: {metricas['total_posts']}")
    lineas.append(
        f"Engagement promedio por post: {metricas['engagement_promedio']:.2f}"
    )
    lineas.append("")

    lineas.append("Número de posts por red:")
    lineas.append(str(df["red"].value_counts()))
    lineas.append("")

    lineas.append("Número de posts por tipo de contenido:")
    lineas.append(str(df["tipo"].value_counts()))
    lineas.append("")

    lineas.append("Engagement promedio por red:")
    lineas.append(str(metricas["eng_por_red"]))
    lineas.append("")

    lineas.append("Engagement promedio por tipo de contenido:")
    lineas.append(str(metricas["eng_por_tipo"]))
    lineas.append("")

    post_top = metricas["post_top"]
    lineas.append("Post con mayor engagement:")
    lineas.append(
        f"- Fecha: {post_top['fecha']}\n"
        f"- Red: {post_top['red']}\n"
        f"- Tipo: {post_top['tipo']}\n"
        f"- Descripción: {post_top['descripcion']}\n"
        f"- Likes: {post_top['likes']}, Comentarios: {post_top['comentarios']}, "
        f"Guardados: {post_top['guardados']}\n"
        f"- Engagement total: {post_top['engagement']}"
    )

    return "\n".join(lineas)


def guardar_reporte(texto: str, ruta_reporte: Path) -> None:
    """
    Guarda el texto en un archivo de reporte.
    """
    ruta_reporte.write_text(texto, encoding="utf-8")
    print(f"\nReporte guardado en: {ruta_reporte.resolve()}")


# -------------------------------------------------------------------
# 5. Punto de entrada
# -------------------------------------------------------------------

def main():
    print(f"Leyendo datos desde: {RUTA_CSV}")
    df = cargar_datos(RUTA_CSV)

    print(f"\nTotal de posts cargados: {len(df)}")
    mostrar_resumen_basico(df)

    metricas = calcular_metricas_engagement(df)
    mostrar_metricas_engagement(metricas)

    reporte = generar_reporte_texto(df, metricas)
    guardar_reporte(reporte, RUTA_REPORTE)


if __name__ == "__main__":
    main()
