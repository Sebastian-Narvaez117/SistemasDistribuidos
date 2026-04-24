import threading
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(threadName)s | %(message)s",
    datefmt="%H:%M:%S",
)

cant_lectores = 0
mutex_lectores = threading.Lock()
sem_escritor = threading.Semaphore(1)
tiempo_lectura = 1
tiempo_escritura = 2

def leer_tablon(id):
    logging.info(f"Lector {id} leyendo")
    time.sleep(tiempo_lectura)

def escribir_tablon(id):
    logging.info(f"Escritor {id} escribiendo")
    time.sleep(tiempo_escritura)


def lector(id):
    global cant_lectores

    # --- Sección de entrada ---
    with mutex_lectores:
        cant_lectores += 1
        logging.info(f"Lector {id} entra | lectores activos: {cant_lectores}")
        if cant_lectores == 1:
            logging.info(f"Lector {id} bloquea al escritor")
            sem_escritor.acquire()

    # --- Sección crítica compartida ---
    leer_tablon(id)

    # --- Sección de salida ---
    with mutex_lectores:
        cant_lectores -= 1
        logging.info(f"Lector {id} sale | lectores activos: {cant_lectores}")
        if cant_lectores == 0:
            logging.info(f"Lector {id} libera al escritor")
            sem_escritor.release()

def escritor(id):
    logging.info(f"Escritor {id} esperando acceso exclusivo")
    sem_escritor.acquire()

    try:
        logging.info(f"Escritor {id} entra a escribir")
        escribir_tablon(id)
    finally:
        logging.info(f"Escritor {id} libera acceso exclusivo")
        sem_escritor.release()

def ejecutar_secuencial():
    inicio = time.perf_counter()

    for i in range(3):
        leer_tablon(i)
    escribir_tablon(1)

    fin = time.perf_counter()
    return fin - inicio


def ejecutar_concurrente():
    global cant_lectores
    cant_lectores = 0

    hilos = []
    inicio = time.perf_counter()

    for i in range(3):
        hilo = threading.Thread(target=lector, args=(i,))
        hilos.append(hilo)
        hilo.start()

    hilo_escritor = threading.Thread(target=escritor, args=(1,))
    hilos.append(hilo_escritor)
    hilo_escritor.start()

    for hilo in hilos:
        hilo.join()
    fin = time.perf_counter()
    return fin - inicio


if __name__ == "__main__":
    logging.info("Iniciando ejecucion secuencial")
    tiempo_secuencial = ejecutar_secuencial()
    logging.info("Iniciando ejecucion concurrente")
    tiempo_concurrente = ejecutar_concurrente()
    logging.info(f"Tiempo secuencial: {tiempo_secuencial:.6f} segundos")
    logging.info(f"Tiempo concurrente: {tiempo_concurrente:.6f} segundos")