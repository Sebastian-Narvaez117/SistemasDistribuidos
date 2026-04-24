
# Practica 3 - Laboratorio Interactivo de Concurrencia

Aplicacion web en Flask para explorar y ejecutar ejercicios de concurrencia en Python.

## Objetivo

Visualizar y ejecutar ejemplos clasicos de sincronizacion de hilos desde una interfaz web:

- Barreras
- Mutex
- Semaforos
- Productor-Consumidor
- Lectores-Escritor

## Estructura

```text
practica3/
├── app.py
├── Encuentro.py
├── Gimnasio.py
├── Lectores.py
├── Panaderia.py
├── Taquilla.py
├── requirements.txt
└── templates/
    ├── detalle.html
    └── index.html
```

## Requisitos

- Python 3.10 o superior
- pip

## Instalacion

Desde la raiz del repositorio:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r practica3/requirements.txt
```

## Ejecucion

1. Inicia la aplicacion:

```bash
python3 practica3/app.py
```

2. Abre en el navegador:

```text
http://127.0.0.1:5000
```

## Funcionalidades de la app

- Lista de ejercicios disponibles.
- Visualizacion del codigo fuente de cada ejercicio.
- Ejecucion de scripts desde la web.
- Reporte de salida estandar, errores y tiempo de ejecucion.

## Ejercicios incluidos

- `Encuentro.py`: sincronizacion por barrera.
- `Gimnasio.py`: semaforos y recursos limitados.
- `Lectores.py`: problema lectores-escritor.
- `Panaderia.py`: productor-consumidor con buffer acotado.
- `Taquilla.py`: mutex y seccion critica.

## Notas

- El timeout de ejecucion esta controlado por la aplicacion web.
- Si cambias codigo en los ejercicios, recarga la pagina para ver la version actualizada.
- Para detener el servidor Flask, usa `Ctrl + C` en la terminal.
