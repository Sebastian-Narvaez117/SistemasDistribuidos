import random
import threading
import time

CAPACIDAD_VITRINA = 10
JORNADA_LABORAL = 20
HAMBRE_CLIENTE = 20

espacios_vacios = threading.Semaphore(CAPACIDAD_VITRINA)
panes_listos = threading.Semaphore(0)
mutex_vitrina = threading.Lock()
vitrina = []
tiempos_horneado = [random.uniform(0.05, 0.2) for _ in range(JORNADA_LABORAL)]
tiempos_comida = [random.uniform(0.05, 0.15) for _ in range(HAMBRE_CLIENTE)]
    

def hornear(n, duracion):
    time.sleep(duracion)
    return f"Pan-{n}"

def comer(pan, duracion):
    print(f"Cliente come {pan}")
    time.sleep(duracion)

def panadero():
    for i in range(1, JORNADA_LABORAL + 1):
        pan = hornear(i, tiempos_horneado[i - 1])

        espacios_vacios.acquire()  # ¿Cabe en la vitrina?
        with mutex_vitrina:  # Abrir vitrina
            vitrina.append(pan)
            print(f"Panadero coloca {pan} | en vitrina: {len(vitrina)}")

        panes_listos.release()  # Avisar al cliente

def cliente():
    for indice in range(HAMBRE_CLIENTE):
        panes_listos.acquire()  # ¿Hay pan disponible?
        with mutex_vitrina:  # Abrir vitrina
            pan = vitrina.pop(0)
            print(f"Cliente retira {pan} | en vitrina: {len(vitrina)}")

        espacios_vacios.release()  # Avisar al panadero
        comer(pan, tiempos_comida[indice])


def ejecutar_secuencial():
    vitrina_secuencial = []
    inicio = time.perf_counter()

    for i in range(1, JORNADA_LABORAL + 1):
        pan = hornear(i, tiempos_horneado[i - 1])
        vitrina_secuencial.append(pan)
        print(f"Panadero coloca {pan} | en vitrina: {len(vitrina_secuencial)}")

        pan = vitrina_secuencial.pop(0)
        print(f"Cliente retira {pan} | en vitrina: {len(vitrina_secuencial)}")
        comer(pan, tiempos_comida[i - 1])

    fin = time.perf_counter()
    return fin - inicio


def ejecutar_concurrente():
    global vitrina
    vitrina = []

    hilo_panadero = threading.Thread(target=panadero)
    hilo_cliente = threading.Thread(target=cliente)

    inicio = time.perf_counter()
    hilo_panadero.start()
    hilo_cliente.start()

    hilo_panadero.join()
    hilo_cliente.join()
    fin = time.perf_counter()

    return fin - inicio

if __name__ == "__main__":
    tiempo_secuencial = ejecutar_secuencial()
    tiempo_concurrente = ejecutar_concurrente()
    print(f"Tiempo secuencial: {tiempo_secuencial:.6f} segundos")
    print(f"Tiempo concurrente: {tiempo_concurrente:.6f} segundos")
    print("Simulacion de panaderia finalizada.")