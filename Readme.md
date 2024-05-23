
# Preparar ambiente base de datos

Para el ejercicio se utiliza Docker con el fin de obtener facilmente una base de datos. La que se emplea es MySQL en su ultima version con el fin de tener los parches de seguridad.
Para instanciar la base de datos se utiliza Docker compose con las siguientes lineas

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

## Configuración de usuario en la base de datos 

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

# Consumo de datos e insercion en base de datos

## Instalar paquetes

Para poder utilizar los scripts, se deben instalar las siguientes librerias con PIP

```
pip install mysql-connector-python
pip install requests
pip install pycryptodome
```

Se generó un script llamado `insertar_datos.py` que consumiera la URL expuesta por el proveedor e insertara los datos en la base de datos
Popular la tabla

```
python insertar_datos.py
```

Creación del repositorio
	* Abrir cuenta en Github
	* Crear un repositorio para la app que sea privado
	* Subir el codigo
