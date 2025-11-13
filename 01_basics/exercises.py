# 01_basics/exercises.py
# Primeros ejercicios de Python – Franco DevAI

# 1) Suma sencilla
def sumar(a, b):
    return a + b

# 2) Convertir CLP a otra moneda (ej: USD)
def clp_a_otra_moneda(monto_clp, tipo_cambio):
    """
    monto_clp: cantidad en pesos chilenos
    tipo_cambio: cuántos CLP equivalen a 1 unidad de la otra moneda (ej: 950 CLP = 1 USD)
    """
    return monto_clp / tipo_cambio

# 3) Calcular porcentaje de gasto
def porcentaje_gasto(monto_gasto, ingreso_mensual):
    """
    Retorna qué porcentaje del ingreso mensual se está yendo en ese gasto.
    """
    if ingreso_mensual == 0:
        return 0
    return (monto_gasto / ingreso_mensual) * 100

# 4) Limpiar nombre de archivo (para librería DJ o documentos)
def limpiar_nombre_archivo(nombre):
    """
    Limpia un nombre de archivo básico:
    - Quita espacios al inicio/fin
    - Reemplaza espacios múltiples por uno solo
    - Convierte a formato 'Title Case'
    """
    nombre = nombre.strip()
    # Reemplazar múltiples espacios por uno solo
    partes = nombre.split()
    nombre_limpio = " ".join(partes)
    return nombre_limpio.title()

# Bloque de prueba
if __name__ == "__main__":
    print("sumar(2, 3) =", sumar(2, 3))
    print("10.000 CLP a USD (tipo de cambio 950) =", clp_a_otra_moneda(10000, 950))
    print("Porcentaje gasto: 50.000 de 300.000 =", porcentaje_gasto(50000, 300000))
    print("Nombre limpio:", limpiar_nombre_archivo("   mi   tema   favorito   .mp3   "))
