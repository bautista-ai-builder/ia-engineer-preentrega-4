# Seguridad

Los administradores usan autenticación multifactor. Los tokens vencen a los treinta minutos y se transmiten mediante HTTPS. Las claves se guardan en un gestor de secretos y rotan cada noventa días. Los logs de autenticación se conservan treinta días. Las copias de seguridad se cifran en reposo.

Los permisos se conceden por rol. Soporte puede leer el estado de un pedido, operaciones revisa métricas y administradores cambian configuraciones; ningún rol de lectura modifica pagos. Las sesiones se invalidan cuando un usuario pierde permisos. Las claves de servicio nunca se incluyen en repositorios, imágenes de contenedor o respuestas de la API. El entorno de desarrollo utiliza credenciales distintas de producción.

Cada intento de acceso fallido registra hora, identificador de usuario y origen de red. Una alerta avisa al equipo ante una serie de intentos fallidos para la misma cuenta. Las copias de respaldo cifradas sólo pueden restaurarse con una cuenta separada. La revisión de permisos se realiza trimestralmente y elimina accesos que ya no sean necesarios.
