from loguru import logger



# Dividir la ruta en días según el número de días especificado
def dividir_en_dias(ruta, num_dias):
    logger.info(f"Dividiendo ruta en {num_dias} días")
    puntos_por_dia = len(ruta) // num_dias
    dias = []

    for i in range(num_dias):
        inicio = i * puntos_por_dia
        fin = inicio + puntos_por_dia
        if i == num_dias - 1:
            dias.append(ruta[inicio:])  # El último día toma los puntos restantes
        else:
            dias.append(ruta[inicio:fin])
    logger.info(f"Ruta dividida en {num_dias} días")
    return dias