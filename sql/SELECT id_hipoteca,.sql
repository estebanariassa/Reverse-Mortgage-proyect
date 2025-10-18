SELECT id_hipoteca,
       codigo_propiedad,
       porcentaje_prestamo,
       tasa_interes,
       plazo_anios,
       renta_mensual,
       deuda_final,
       fecha_inicio,
       fecha_fin,
       estado
FROM public.hipotecas
LIMIT 1000;