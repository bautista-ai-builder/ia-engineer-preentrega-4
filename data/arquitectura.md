# Arquitectura de pedidos

La API de pedidos usa FastAPI y PostgreSQL. PostgreSQL es la fuente de verdad para pedidos, pagos y estados. Redis funciona como caché y puede reconstruirse desde la base de datos. Un pedido recibe un identificador único. Las escrituras se realizan en transacciones para evitar estados parciales. El balanceador consulta el endpoint de disponibilidad antes de enviar tráfico.

Cada solicitud lleva un identificador de correlación que se conserva en los logs de la API y en los eventos de negocio. La creación de pedidos usa una clave de idempotencia: si un cliente repite la solicitud después de un timeout, el servidor devuelve el mismo pedido en vez de crear otro. El proceso de pagos se desacopla mediante una cola; el estado del pedido pasa de pendiente a pagado sólo después de recibir la confirmación. La caché de Redis usa un tiempo de vida de diez minutos para las consultas frecuentes y se invalida cuando cambia un pedido.

La versión nueva del servicio se despliega después de aplicar migraciones compatibles con la versión anterior. El endpoint de salud indica si el proceso responde; el de disponibilidad comprueba PostgreSQL y los recursos necesarios para aceptar tráfico. Los errores de escritura se devuelven con un código HTTP adecuado y un mensaje seguro, sin exponer cadenas de conexión ni trazas internas.
