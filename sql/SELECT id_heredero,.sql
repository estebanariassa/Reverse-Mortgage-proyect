SELECT id_heredero,
       cedula_cliente,
       nombre,
       relacion,
       telefono,
       correo
FROM public.herederos
LIMIT 1000;