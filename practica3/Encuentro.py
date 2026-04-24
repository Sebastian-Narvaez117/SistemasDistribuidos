import threading
import time

contador = 0
N_TOTAL = 5

mutex = threading.Lock()
condicion = threading.Condition(mutex)
tiempo_fase = 0.05

def llegar_barrera(id_hilo):
    global contador

    time.sleep(tiempo_fase)
    
    with mutex:
        contador = contador + 1

        if contador == N_TOTAL:
            condicion.notify_all()
        else:
            while contador < N_TOTAL:
                condicion.wait()

    print("Hilo", id_hilo, "pasa a fase 2")


def ejecutar_concurrente():
    global contador
    contador = 0

    hilos = []
    inicio = time.perf_counter()

    for i in range(N_TOTAL):
        hilo = threading.Thread(target=llegar_barrera, args=(i,))
        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()

    fin = time.perf_counter()
    return fin - inicio

def ejecutar_secuencial():
    inicio = time.perf_counter()
    for i in range(N_TOTAL):
        time.sleep(tiempo_fase)
        print("Hilo", i, "pasa a fase 2")
    fin = time.perf_counter()
    return fin - inicio

if __name__ == "__main__":
    tiempo_secuencial = ejecutar_secuencial()
    tiempo_concurrente = ejecutar_concurrente()
    print(f"Tiempo secuencial: {tiempo_secuencial:.6f} segundos")
    print(f"Tiempo concurrente: {tiempo_concurrente:.6f} segundos")