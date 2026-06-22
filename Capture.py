#!/usr/bin/env python3
"""Captura rapida para el segundo cerebro.

Uso:
    python Capture.py "tu idea o tarea"
    python Capture.py "llamar al especialista" -a salud

Agrega una linea con la hora (y un area opcional) a la nota diaria en
VAULT/Diario/AAAA-MM-DD.md. Si la nota del dia no existe, la crea.
"""
import os
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

VAULT_DIR = os.environ.get("VAULT_DIR")
if not VAULT_DIR:
    raise SystemExit(
        "Error: No se encontro VAULT_DIR en el archivo .env\n"
        "Agrega esta linea a tu .env:\n"
        r"VAULT_DIR=C:\Users\ADMIN\Documents\segundo-cerebro"
    )
VAULT = Path(VAULT_DIR)

AREAS = (
    "cuerpo, mente, carrera, negocios, relaciones, "
    "entrenamiento, nutricion, sueno, salud, salud-mental, "
    "estudio, trabajo, clientes, economia, arizona-meals, "
    "airbnb, ingenieria, pareja, familia, red-social"
)


def main():
    p = argparse.ArgumentParser(description="Captura rapida al segundo cerebro")
    p.add_argument("texto", help="La idea, tarea o nota a capturar")
    p.add_argument("-a", "--area", default="", help=f"Area opcional: {AREAS}")
    args = p.parse_args()

    if not VAULT.exists():
        raise SystemExit(f"Error: El vault no existe en {VAULT}")

    ahora = datetime.now()
    diario = VAULT / "Diario"
    diario.mkdir(parents=True, exist_ok=True)
    archivo = diario / f"{ahora:%Y-%m-%d}.md"

    if not archivo.exists():
        archivo.write_text(f"# {ahora:%Y-%m-%d}\n\n## Capturas\n", encoding="utf-8")

    etiqueta = f"({args.area}) " if args.area else ""
    linea = f"- {ahora:%H:%M} {etiqueta}{args.texto}\n"
    with archivo.open("a", encoding="utf-8") as f:
        f.write(linea)

    print(f"Guardado en {archivo}")


if __name__ == "__main__":
    main()