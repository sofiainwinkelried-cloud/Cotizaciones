# Cotizaciones — Uber vs DiDi vs Cabify (Córdoba)

Repositorio para analizar las cotizaciones que se capturan automáticamente
con MacroDroid en 4 rutas de referencia en Córdoba (2 cortas, 2 largas; en
cada par, una con mucha demanda real y otra con poca).

Fuente de datos: [planilla "Cotizaciones"](https://docs.google.com/spreadsheets/d/1SLtiQSFMCUntwpxdMmR6RSDsgNADXc4-Gu9_aSc15oo/edit?gid=0#gid=0).
DiDi todavía no está capturando datos (pendiente de configurar MacroDroid).

## Rutas de referencia

| Tipo  | Demanda real       | Origen                          | Destino                     |
|-------|---------------------|----------------------------------|------------------------------|
| Corta | Muchas estimaciones | Crisol 64                        | Plaza Colón                  |
| Corta | Pocas estimaciones  | Javier Lascano Colodrero 2924     | Ilolay 3000                  |
| Larga | Muchas estimaciones | Obispo Salguero 777              | Av. Octavio Pinto 2541       |
| Larga | Pocas estimaciones  | Av. Rufino Varela Ortiz 5147     | Santa Fe 330                 |

## Estructura

- `data/raw/` — exports crudos de la planilla de Google Sheets (uno por corrida/fecha).
- `scripts/analizar_cotizaciones.py` — limpia un export y genera un reporte en markdown
  (precio promedio por ruta/hora, gap Cabify vs Uber, disponibilidad de precio).
- `reports/` — reportes generados, uno por fecha de análisis.

## Cómo actualizar el análisis

1. Exportar la hoja de Sheets como CSV (Archivo > Descargar > CSV) y guardarla en
   `data/raw/cotizaciones_<fecha>.csv`.
2. Correr:

   ```bash
   python3 scripts/analizar_cotizaciones.py data/raw/cotizaciones_<fecha>.csv \
       --out reports/<fecha>-analisis.md
   ```

3. Revisar el reporte generado y, si aporta, actualizar los hallazgos en
   `reports/`.

## Limitaciones actuales

- Todavía hay muy pocos días de historia (menos de 24 hs continuas), por lo
  que **no** se pueden sacar conclusiones confiables de día de semana,
  principio/mediados de mes, ni semana calendario. El pipeline ya está
  armado para esos cortes; solo hace falta que se acumulen más días.
- DiDi no tiene datos todavía.
- Cuando haya suficiente historia, se puede cruzar con la planilla de
  [drivers/oferta](https://docs.google.com/spreadsheets/d/1e9z_TESDjP-tB2OzHPFpvV6cZWMFkWZ5qYIYKPCbj9s/edit?gid=1693516104#gid=1693516104)
  para relacionar comportamiento de precios con oferta de conductores.
