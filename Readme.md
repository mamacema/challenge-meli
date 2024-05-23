
# Preparación del ambiente

## base de datos

Para el ejercicio se utiliza Docker con el fin de obtener fácilmente una base de datos. La que se emplea es MySQL en su ultima versión con el fin de tener los parches de seguridad.
Para instanciar la base de datos se utiliza Docker compose con las siguientes líneas

```
version: '3.1'

services:

  db:
    image: mysql
    environment:
      MYSQL_ROOT_PASSWORD: hcO/rG0HsJLv+dXv
    ports:
      - "3306:3306"
```

Se inicializa la base de datos desde el directorio donde se encuentre el archivo `docker-compose.yaml` que contiene la información para inicializar el contenedor con el siguiente comando

```
docker compose up -d
```

Nota: la opción `-d` significa `detach` o `correr en background`

Se valida que el contenedor con la base de datos este arriba

```
docker compose ps
```

### Configuración de usuario en la base de datos 

1. Se ingresar a la base de datos

    Se ingresa al contenedor a traves de `bash`

    ```
    docker exec -it appconsumousuarios-db-1 bash
    ```

    Una vez en el promt del contenedor, se ejecuta el siguiente comando

    ```
    mysql -uroot -p
    ```

2. Se crear la base de datos

    ```
    create database repositorio;
    ```

3. Se crea usuario de la app

    ```
    USE repositorio;
    CREATE USER 'usermanager'@'%' IDENTIFIED BY 'hcO/rG0HsJLv+dXv';
    GRANT ALL PRIVILEGES ON repositorio.* TO 'usermanager'@'%';
    FLUSH PRIVILEGES;

    SHOW GRANTS FOR 'usermanager';
    ```

4. Se ejecuta el script `crear_tabla.py` para crear la tabla en la base de datos

    ```
    python crear_tabla.py
    ```

### Instalar paquetes Python

Para poder utilizar los scripts, se deben instalar las siguientes librerias con PIP

```
pip install mysql-connector-python
pip install requests
pip install pycryptodome
```

## Consumo de datos e insercion en base de datos

### Ejecución del script

Se generó un script llamado `insertar_datos.py` que consumiera la URL expuesta por el proveedor e insertara los datos en la base de datos

Popular la tabla

```
python insertar_datos.py
```

# Supuestos y problemas

Si bien mi experiencia principal no se centra en el desarrollo, la administración de bases de datos o la gestión de infraestructuras, poseo un conocimiento integral sobre su funcionamiento, interacción y los requisitos de seguridad necesarios para su desarrollo y despliegue efectivos.

## Base de datos

Como se menciona en la sección de configuración, se utiliza `docker` + `docker compose` para el despliegue. Hay ciertas configuración que se realizarón y no son correctas:

* Aunque se utiliza una contraseña que contiene 16 caracteres y combina minusculas, mayusculas, numeros y caracteres especiales, la contraseña del usuario root se deja guardada en el archivo, lo anterior es mala practica porque este irá al repositorio y es muy fácil de acceder, se hace de esta forma ya que integrar la aplicación con un servicio como AWS Secret Manager tomaría mas tiempo y esta fuera del alcance de este challenge.
* El usuario que realiza la lectura y escritura de la información es el mismo y sus credenciales también se encuentra expuestas en el código, aunque es una mala practica y no va de acuerdo con las normas y estándares, se realiza por practicidad.
* El usuario creado para interactuar con la base de datos se le asignaron todos los privilegios y peor aún, lo puede realizar desde cualquier host, lo anterior también es categorizado como una mala practica ya que no hay gestión sobre los acceso privilegiados.
* Cero hardenizado cuando se realiza la configuración la base de datos para que registre y audite todas las actividades de los usuarios, incluidos los intentos de acceso, consultas ejecutadas y cambios realizados en los datos.


Ninguno de los puntos anteriores es considerado una buenas practica y es evidente el riesgo a nivel de seguridad que implementar en un ambiente de pruebas o productivo generaría.

## Ejecución del contenedor

Consideraciones de seguridad implementadas:

* Utiliza una imagen de contenedor proveniente de fuentes confiables y verificadas - Docker Hub.
* Uso de imagen de contenedor actualizada con parches de seguridad y actualizaciones de software para evitar vulnerabilidades conocidas debido al uso de una imagen oficial y verificada, entregada por el proveedor a través de Docker Hub.

Consideraciones de seguridad que no se implementaron sobre el contenedor:

* No se implementó ninguna herramientas de gestión de secretos para manejar de forma segura credenciales y otros datos sensibles utilizados por la aplicación dentro del contenedor.
* No se Limitó los privilegios del contenedor para reducir el impacto de posibles ataques.
* Para los recursos, no se utilizaron medidas de aislamiento para limitar el acceso del contenedor a los recursos del sistema y para prevenir la interferencia entre contenedores o en este caso la maquina donde fue desplegado.
* No se cuenta con un sistema de monitoreo y registro para supervisar la actividad del contenedor y detectar posibles intrusiones o comportamientos anómalos.
* Cero implementación políticas de seguridad de red para restringir el tráfico entrante y saliente del contenedor, y utiliza medidas como firewalls y listas de control de acceso para protegerlo de ataques externos.

## Consumo de servicio expuesto por el proveedor

Dado que la conexión se debe dar hacia el proveedor externo y este es el encargado inicial de salvaguardar la información de los datos de tarjetas de los clientes, se debe exigir a este cumplir con los estándares antes de iniciar la transmisión y almacenamiento de los datos y asi evitar un riesgo reputacional intangible en caso de que esa información se llegue a ver comprometida

## Manejo de llaves de cifrado

En Python utiliza el paquete `pycryptodome` para realizar el cifrado de lo que se consideran datos sensibles.

* No hay gestión segura de claves, como se menciona anteriormente no existe integración de un servicio como el de AWS Secret Manager para este item y la llave se encuentra expuesta en el código.
* Aunque la clave generada es aleatoria y se utiliza un vector de inicialización diferente (IV) durante cada transacción, no es lo suficientemente robusta para el manejo de datos tan sensibles como los que expone el proveedor debido a que su longitud es bastante corta aunque AES sea un algoritmo que pueda funcionar para este caso.
* Otra consideración que no se tuvo en cuenta durante este ejercicio es que solo se implementa AES_CBC para cifrado de datos sensibles, pero solo podría generar riesgos o dar cabida a ataques como modificación de texto cifrado, por lo que es recomendable combinar con otro esquema de relleno seguro como PKCS7.

## Manejo de credenciales y usuarios

## Manejo de errores

* Cero código para el manejo de errores, por lo tanto si se presenta algún error y la aplicación se rompe, puede que se expongan datos sensibles o incluso contraseñas
* En general la aplicación no cuenta con cifrado de datos entre sus capas, no tiene pruebas exhaustivas que garantice su funcionamiento y seguridad en las diferentes etapas

