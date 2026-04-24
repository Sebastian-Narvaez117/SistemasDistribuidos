import random
import threading
import time

in_use = 0
max_in_use = 0
stats_lock = threading.Lock()

class MiSemaforo:
    def __init__(self, valor_inicial):
        self.contador = valor_inicial
        self.cerrojo = threading.Lock()
        self.cola_espera = threading.Condition(self.cerrojo)

    def esperar(self):
        with self.cerrojo:
            while self.contador == 0:
                self.cola_espera.wait()
            self.contador -= 1

    def senial(self):
        with self.cerrojo:
            self.contador += 1
            self.cola_espera.notify()


N_MAQUINAS = 3
N_ATLETAS = 7
semaforo = MiSemaforo(N_MAQUINAS)
duraciones_uso = [random.uniform(0.5, 1.5) for _ in range(N_ATLETAS)]


def atleta(nombre, duracion):
    global in_use, max_in_use

    print(f"{nombre} esperando máquina")
    semaforo.esperar()  # wait()
    try:
        with stats_lock:
            in_use += 1
            max_in_use = max(max_in_use, in_use)
        print(f"{nombre} usando máquina")
        time.sleep(duracion)
    finally:
        with stats_lock:
            in_use -= 1
        print(f"{nombre} liberando máquina")
        semaforo.senial()  # signal()


def ejecutar_secuencial():
    inicio = time.perf_counter()
    for i, duracion in enumerate(duraciones_uso):
        print(f"Atleta-{i} esperando máquina")
        print(f"Atleta-{i} usando máquina")
        time.sleep(duracion)
        print(f"Atleta-{i} liberando máquina")
    fin = time.perf_counter()
    return fin - inicio


def ejecutar_concurrente():
    inicio = time.perf_counter()
    global in_use, max_in_use
    in_use = 0
    max_in_use = 0
    hilos = [
        threading.Thread(target=atleta, args=(f"Atleta-{i}", duracion))
        for i, duracion in enumerate(duraciones_uso)
    ]
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
    fin = time.perf_counter()
    return fin - inicio


if __name__ == "__main__":
    tiempo_secuencial = ejecutar_secuencial()
    tiempo_concurrente = ejecutar_concurrente()
    print(f"Tiempo secuencial: {tiempo_secuencial:.6f} segundos")
    print(f"Tiempo concurrente: {tiempo_concurrente:.6f} segundos")
    print(f"Maximo de recursos en uso: {max_in_use}")