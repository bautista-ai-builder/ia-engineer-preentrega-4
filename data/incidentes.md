# Gestión de incidentes

Un incidente de exposición de datos se escala inmediatamente al responsable de seguridad. El equipo revoca credenciales comprometidas, preserva evidencia y revisa el alcance. Para una caída de la base de datos, el operador revisa conexiones, almacenamiento y logs; después verifica la consistencia de los pedidos pendientes antes de reanudar el tráfico.

La persona de guardia registra el momento de detección, el síntoma observado y las acciones ejecutadas. Primero se limita el impacto: puede bloquearse una credencial, retirar una instancia del balanceador o suspender escrituras. Después se investiga la causa sin borrar logs ni alterar la evidencia. El responsable de seguridad decide la comunicación necesaria según el alcance confirmado del evento.

Cuando el servicio vuelve a estar estable, el equipo valida consultas y operaciones de extremo a extremo. Se compara una muestra de pedidos con los registros de pagos para detectar inconsistencias. El informe posterior describe causa raíz, duración, usuarios afectados, medidas correctivas y responsables. Las acciones preventivas se siguen hasta su cierre y se incorporan a los procedimientos de operación.
