# Operación y respaldos

PostgreSQL genera un respaldo completo cada noche a las 02:00 UTC. Se conservan siete copias. El objetivo de recuperación es cuatro horas y la pérdida máxima tolerada es de veinticuatro horas. Se ensaya una restauración mensual. Si PostgreSQL falla, la API suspende escrituras hasta recuperar la conexión.

El operador comprueba cada mañana que el respaldo anterior terminó correctamente y que su tamaño se encuentra dentro del rango esperado. Una prueba mensual restaura una copia en un entorno aislado, ejecuta consultas de integridad y documenta el tiempo de recuperación. Si la restauración falla, se abre un incidente y se conserva el último respaldo verificado hasta resolverlo. Redis no requiere restauración porque sus entradas se recomponen desde PostgreSQL.

Durante una caída de la base, el balanceador mantiene sólo las instancias con disponibilidad confirmada. El equipo revisa conexiones, almacenamiento, réplicas y logs. Antes de volver a habilitar escrituras, compara pedidos pendientes, totales de pagos y el último evento procesado. El responsable del incidente registra la línea de tiempo y comunica cuándo se recuperó el servicio.
