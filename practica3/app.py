from pathlib import Path
import subprocess
import sys
import time

from flask import Flask, abort, jsonify, render_template

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
PROYECTO_NOMBRE = "Laboratorio Interactivo de Concurrencia"
PROYECTO_SUBTITULO = "Explora mutex, semaforos, barreras y sincronizacion de hilos"
TIMEOUT_EJECUCION_SEG = 60
EJERCICIOS = [
    {
        "archivo": "Encuentro.py",
        "titulo": "Sincronizacion por Barrera",
        "descripcion": "Todos los hilos esperan hasta que el grupo completo este listo.",
    },
    {
        "archivo": "Gimnasio.py",
        "titulo": "Semaforos y Recursos Limitados",
        "descripcion": "Control de maquinas compartidas con un semaforo personalizado.",
    },
    {
        "archivo": "Lectores.py",
        "titulo": "Problema Lectores-Escritor",
        "descripcion": "Lecturas concurrentes y escritura exclusiva sobre un tablon.",
    },
    {
        "archivo": "Panaderia.py",
        "titulo": "Productor-Consumidor",
        "descripcion": "Buffer acotado con semaforos para coordinar produccion y consumo.",
    },
    {
        "archivo": "Taquilla.py",
        "titulo": "Mutex y Seccion Critica",
        "descripcion": "Incremento concurrente seguro en una taquilla de ventas.",
    },
]
EJERCICIOS_PERMITIDOS = {ejercicio["archivo"] for ejercicio in EJERCICIOS}


def _obtener_archivos() -> list[dict]:
    directorio = BASE_DIR
    archivos = []

    for ruta in sorted(directorio.iterdir()):
        if not ruta.is_file():
            continue
        if ruta.suffix not in {".py", ".txt"}:
            continue

        archivos.append(
            {
                "nombre": ruta.name,
                "ruta_relativa": ruta.name,
            }
        )

    return archivos


def _ejecutar_ejercicio(nombre_archivo: str) -> dict:
    if nombre_archivo not in EJERCICIOS_PERMITIDOS:
        abort(404)

    ruta = (BASE_DIR / nombre_archivo).resolve()
    if BASE_DIR not in ruta.parents or not ruta.exists() or not ruta.is_file():
        abort(404)

    inicio = time.perf_counter()

    try:
        resultado = subprocess.run(
            [sys.executable, str(ruta)],
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            timeout=TIMEOUT_EJECUCION_SEG,
            check=False,
        )
    except subprocess.TimeoutExpired:
        duracion = time.perf_counter() - inicio
        return {
            "ok": False,
            "codigo": None,
            "duracion": round(duracion, 3),
            "salida": "",
            "error": (
                f"Tiempo limite superado: {TIMEOUT_EJECUCION_SEG} segundos. "
                "Reduce la carga del ejercicio o aumenta el timeout."
            ),
        }

    duracion = time.perf_counter() - inicio
    return {
        "ok": resultado.returncode == 0,
        "codigo": resultado.returncode,
        "duracion": round(duracion, 3),
        "salida": resultado.stdout,
        "error": resultado.stderr,
    }


def _leer_archivo(nombre_archivo: str) -> str:
    ruta = (BASE_DIR / nombre_archivo).resolve()

    # Evita path traversal: el archivo siempre debe quedar dentro de practica3.
    if BASE_DIR not in ruta.parents:
        abort(404)
    if not ruta.exists() or not ruta.is_file():
        abort(404)

    return ruta.read_text(encoding="utf-8")


@app.route("/")
def index():
    return render_template(
        "index.html",
        nombre_proyecto=PROYECTO_NOMBRE,
        subtitulo_proyecto=PROYECTO_SUBTITULO,
        ejercicios=EJERCICIOS,
    )


@app.route("/archivo/<nombre_archivo>")
def ver_archivo(nombre_archivo: str):
    contenido = _leer_archivo(nombre_archivo)
    return render_template(
        "detalle.html",
        proyecto=PROYECTO_NOMBRE,
        nombre_archivo=nombre_archivo,
        contenido=contenido,
    )


@app.post("/ejecutar/<nombre_archivo>")
def ejecutar(nombre_archivo: str):
    return jsonify(_ejecutar_ejercicio(nombre_archivo))


if __name__ == "__main__":
    app.run(debug=True)
