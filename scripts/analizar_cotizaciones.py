#!/usr/bin/env python3
"""
Analiza exports de la hoja "Cotizaciones" (Crisol/Uber/DiDi capturados con MacroDroid).

Uso:
    python3 scripts/analizar_cotizaciones.py data/raw/cotizaciones_2026-07-28.csv \
        --out reports/2026-07-28-analisis-inicial.md

El export de Google Sheets tiene una particularidad: la columna Distance usa
coma decimal ("3,9" = 3.9 km), lo cual rompe un CSV separado por comas si no
viene bien "quoteado". Este script asume el CSV tal como lo entrega Sheets
(exportado con comillas en esos campos). Si el export viene "roto" (columnas
corridas), primero hay que volver a exportarlo desde Sheets como CSV real.
"""
import argparse
import sys
from pathlib import Path

import pandas as pd

RUTA_NOMBRES = {
    ("Crisol 64", "Plaza Colón"): "Crisol 64 -> Plaza Colón (corta, muchas est.)",
    ("Javier Lascano Colodrero 2924", "Ilolay 3000"): "Lascano Colodrero -> Ilolay (corta, pocas est.)",
    ("Obispo Salguero 777", "Av. Octavio Pinto 2541"): "Obispo Salguero -> Octavio Pinto (larga, muchas est.)",
    ("Av. Rufino Varela Ortiz 5147", "Santa Fe 330"): "Rufino Varela -> Santa Fe (larga, pocas est.)",
}


def cargar(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="utf-8")
    df.columns = [c.strip() for c in df.columns]

    df["Fecha"] = pd.to_datetime(df["Fecha"], format="%d/%m/%Y %H:%M:%S")
    df["Distance_km"] = (
        df["Distance"].astype(str).str.replace(",", ".", regex=False).astype(float)
    )
    df["Ruta"] = df.apply(
        lambda r: RUTA_NOMBRES.get((r["Origen"], r["Destino"]), f'{r["Origen"]} -> {r["Destino"]}'),
        axis=1,
    )
    df["Hora"] = df["Fecha"].dt.hour
    df["DiaSemana"] = df["Fecha"].dt.day_name(locale="es_ES.utf8") if False else df["Fecha"].dt.day_name()
    df["Dia"] = df["Fecha"].dt.date
    df["gap_pct"] = (df["Precio Cabify"] - df["Precio Uber"]) / df["Precio Uber"] * 100
    return df


def reporte(df: pd.DataFrame) -> str:
    lineas = []
    lineas.append(f"Rango de datos: {df['Fecha'].min()} -> {df['Fecha'].max()}")
    lineas.append(f"Filas totales: {len(df)}")
    dias_cubiertos = df["Dia"].nunique()
    lineas.append(f"Dias calendario distintos cubiertos: {dias_cubiertos}")
    lineas.append("")

    lineas.append("## Disponibilidad de precio (no nulos)")
    for col in ["Precio Cabify", "Precio Uber", "Precio DiDi"]:
        lineas.append(f"- {col}: {df[col].notna().sum()} / {len(df)}")
    lineas.append("")

    lineas.append("## Estadisticas por ruta")
    stats = df.groupby("Ruta").agg(
        n=("Precio Cabify", "size"),
        cabify_prom=("Precio Cabify", "mean"),
        uber_prom=("Precio Uber", "mean"),
        gap_prom_pct=("gap_pct", "mean"),
        gap_min_pct=("gap_pct", "min"),
        gap_max_pct=("gap_pct", "max"),
    ).round(1)
    lineas.append(stats.to_markdown())
    lineas.append("")

    lineas.append("## Precio Cabify promedio por hora del dia y ruta")
    pivot_c = df.pivot_table(index="Hora", columns="Ruta", values="Precio Cabify", aggfunc="mean").round(0)
    lineas.append(pivot_c.to_markdown())
    lineas.append("")

    lineas.append("## Precio Uber promedio por hora del dia y ruta")
    pivot_u = df.pivot_table(index="Hora", columns="Ruta", values="Precio Uber", aggfunc="mean").round(0)
    lineas.append(pivot_u.to_markdown())
    lineas.append("")

    if dias_cubiertos > 1:
        lineas.append("## Precio promedio por dia de semana (Cabify)")
        pivot_dow = df.pivot_table(index="DiaSemana", columns="Ruta", values="Precio Cabify", aggfunc="mean").round(0)
        lineas.append(pivot_dow.to_markdown())
        lineas.append("")
    else:
        lineas.append("## Dia de semana / quincena / mes")
        lineas.append(
            "Todavia no hay suficientes dias distintos en los datos para "
            "analizar patrones por dia de semana, principio/mediados de mes "
            "o semana calendario. Volver a correr este script cuando haya "
            "mas dias acumulados."
        )
        lineas.append("")

    return "\n".join(lineas)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input_csv")
    ap.add_argument("--out", default=None, help="Path de salida para el reporte en markdown")
    args = ap.parse_args()

    df = cargar(args.input_csv)
    texto = reporte(df)

    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(texto, encoding="utf-8")
        print(f"Reporte escrito en {args.out}", file=sys.stderr)
    else:
        print(texto)


if __name__ == "__main__":
    main()
