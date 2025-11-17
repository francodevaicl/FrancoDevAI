
# practica_bloque1.py – práctica de variables y funciones

# 1) Variables
ingreso_mensual = 300000
gasto_comida = 50000
gasto_transporte = 20000

# 2) Cálculo
gasto_total = gasto_comida + gasto_transporte
ahorro = ingreso_mensual - gasto_total

print("Ingreso mensual:", ingreso_mensual)
print("Gasto total:", gasto_total)
print("Ahorro estimado:", ahorro)

# 3) Función para calcular ahorro
def calcular_ahorro(ingreso, gasto_total):
    return ingreso - gasto_total

ahorro_funcion = calcular_ahorro(ingreso_mensual, gasto_total)
print("Ahorro calculado con función:", ahorro_funcion)

# 4) Función de porcentaje
def porcentaje_gasto(monto, ingreso):
    if ingreso == 0:
        return 0
    return (monto / ingreso) * 100

porcentaje_comida = porcentaje_gasto(gasto_comida, ingreso_mensual)
print("Porcentaje del ingreso gastado en comida:", porcentaje_comida)