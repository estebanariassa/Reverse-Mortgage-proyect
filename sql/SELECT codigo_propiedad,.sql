SELECT codigo_propiedad,
       cedula_cliente,
       valor_propiedad,
       direccion,
       area,
       tipo
FROM public.propiedades
LIMIT 1000;