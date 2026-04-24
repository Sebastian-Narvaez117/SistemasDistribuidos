import threading
import time

N_HILOS  = 5
M_VENTAS = 1_000_000
N_EJECUCIONES = 10
mutex = threading.Lock()
boletos_vendidos = 0

def vender():
    global boletos_vendidos
    for _ in range(M_VENTAS):
        with mutex:
            boletos_vendidos += 1

def ejecutar_concurrente():
    global boletos_vendidos
    boletos_vendidos = 0

    inicio = time.perf_counter()
    hilos = [threading.Thread(target=vender) for _ in range(N_HILOS)]
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
    fin = time.perf_counter()

    if boletos_vendidos == N_HILOS * M_VENTAS:
        return fin - inicio, boletos_vendidos
    else:
        raise ValueError("Inconsistencia en el número de boletos vendidos")






def ejecutar_secuencial():
    global boletos_vendidos
    boletos_vendidos = 0

    inicio = time.perf_counter()
    for _ in range(N_HILOS * M_VENTAS):
        boletos_vendidos += 1
    fin = time.perf_counter()

    if boletos_vendidos == N_HILOS * M_VENTAS:
        return fin - inicio, boletos_vendidos
    else:
        raise ValueError("Inconsistencia en el número de boletos vendidos")
def ejecutar_10_veces():
    resultados = []

    for ejecucion in range(1, N_EJECUCIONES + 1):
        tiempo_secuencial, total_secuencial = ejecutar_secuencial()
        tiempo_concurrente, total_concurrente = ejecutar_concurrente()

        resultados.append((total_secuencial, total_concurrente))

        print(
            f"Ejecucion {ejecucion:02d} | "
            f"Secuencial: {total_secuencial} en {tiempo_secuencial:.6f} s | "
            f"Concurrente: {total_concurrente} en {tiempo_concurrente:.6f} s"
        )

    consistentes = all(
        secuencial == N_HILOS * M_VENTAS and concurrente == N_HILOS * M_VENTAS
        for secuencial, concurrente in resultados
    )


if __name__ == "__main__":
    ejecutar_10_veces()