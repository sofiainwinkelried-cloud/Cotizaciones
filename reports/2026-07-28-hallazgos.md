# Hallazgos iniciales — 27/07 al 28/07/2026

Ventana de datos: 27/07 15:49 hs a 28/07 10:08 hs (92 cotizaciones, ~19 horas
continuas). Tabla completa de números en
[`2026-07-28-analisis-inicial.md`](2026-07-28-analisis-inicial.md).

## Lo que todavía NO se puede decir

Con menos de un día completo de historia no hay manera de comparar días de
semana, principio/mediados de mes ni semanas calendario — solo hay una
ventana continua (tarde/noche del lunes 27 + madrugada/mañana del martes
28). El script y la estructura de carpetas ya están listos para ese corte;
en cuanto haya ~2-3 semanas de datos acumulados va a valer la pena repetir
este análisis con eso en foco. DiDi todavía no tiene datos (falta activar
esa captura en MacroDroid).

## Lo que sí se ve con lo que hay

**1. Cabify es más barata que Uber en 3 de las 4 rutas, en promedio.**

| Ruta | Gap promedio Cabify vs Uber |
|---|---|
| Crisol → Plaza Colón (corta, mucha demanda) | **+4,2%** (empatada / levemente más cara) |
| Lascano Colodrero → Ilolay (corta, poca demanda) | **-16,6%** (Cabify más barata) |
| Obispo Salguero → Octavio Pinto (larga, mucha demanda) | **-14,1%** (Cabify más barata) |
| Rufino Varela → Santa Fe (larga, poca demanda) | **-23,9%** (Cabify bastante más barata) |

(Gap = (Precio Cabify − Precio Uber) / Precio Uber. Negativo = Cabify más
barata que Uber en ese momento.)

**2. La ruta con más demanda real es, en las dos distancias, la que menos
diferencia de precio tiene entre Cabify y Uber.** Crisol/Plaza Colón (mucha
demanda) está prácticamente empatada con Uber; Lascano/Ilolay (poca demanda)
tiene a Cabify 16,6 puntos más barata en promedio. Mismo patrón en las
largas: Obispo Salguero (mucha demanda) -14,1% vs Rufino Varela (poca
demanda) -23,9%. Hipótesis a confirmar con más datos: en las rutas de poca
demanda hay menos autos cerca y el algoritmo de Uber reacciona con precios
más altos, mientras que Cabify no ajusta tanto.

**3. Hay una ventana de mayor volatilidad entre 00:00 y 02:00 hs, sobre
todo en las rutas largas.** Ejemplos:
- Rufino Varela → Santa Fe: Uber promedia ~7.000-7.700 en la tarde/noche
  (15-23 hs) pero salta a 8.100-11.550 entre la 01 y las 02 hs, con un pico
  puntual de **$20.100** a las 23:08 (vs. Cabify $4.600 en esa misma
  cotización — el gap más negativo de todo el dataset, -77%).
- Obispo Salguero → Octavio Pinto: Uber pasa de ~6.000-7.250 en la tarde a
  **$11.600** a las 00:00 hs.
- En esa misma franja horaria también hay un pico de Cabify (no de Uber):
  a las 00:32 hs, Crisol → Plaza Colón, Cabify pidió $7.400 contra $3.700
  de Uber (+100%, el gap más positivo del dataset). O sea que la
  madrugada es más volátil en general, no que una sola plataforma sea
  siempre la que sube.

**4. Cabify no siempre devuelve precio; Uber casi siempre sí.** Cabify no
tuvo estimación en 13 de 92 cotizaciones (14%), repartidas entre las 4
rutas y concentradas un poco más entre las 23-02 hs y 16-20 hs. Uber faltó
en solo 4 de 92 (4%). DiDi: 0 de 92 (sin capturar todavía). Ojo con la
columna "Cabify vs Uber" de la planilla original: cuando falta el precio de
Cabify, esa columna muestra "-100%" como si fuera un dato real de
comparación, cuando en realidad es solo un artefacto de la fórmula por
celda vacía — conviene no contar esos "-100%" como caídas de precio reales.

**5. Precio por km: Cabify tiende a cobrar menos por km que Uber,
especialmente en las rutas largas** (Cabify ~$792-798/km en las largas vs.
Uber ~$940-1.110/km; en las cortas están más parejos, ~$976-986/km Cabify
vs. $964-1.197/km Uber). Es coherente con el punto 1: a mayor distancia,
mayor ventaja relativa de precio para Cabify en estas rutas.

## Próximos pasos sugeridos

1. Dejar correr la captura (Uber, y sumar DiDi en cuanto esté andando en
   MacroDroid) durante 2-3 semanas para poder mirar día de semana,
   principio/mediados de mes.
2. Repetir el análisis con `scripts/analizar_cotizaciones.py` sobre el
   export acumulado.
3. Cuando haya volumen, cruzar con la planilla de oferta de drivers para
   ver si los gaps de precio y los picos de madrugada se explican por
   caída de oferta de conductores en esas rutas/horarios.
