import mysql.connector

# Conectar a la base de datos
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="usermanager",
    password="hcO/rG0HsJLv+dXv",
    database="repositorio"
)

# Crear un cursor
cursor = conn.cursor()

# Crear una tabla si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    fec_alta DATETIME,
                    user_name VARCHAR(255),
                    codigo_zip VARCHAR(255),
                    credit_card_num VARCHAR(255),
                    credit_card_ccv VARCHAR(255),
                    cuenta_numero VARCHAR(255),
                    direccion VARCHAR(255),
                    geo_latitud VARCHAR(255),
                    geo_longitud VARCHAR(255),
                    color_favorito VARCHAR(255),
                    foto_dni VARCHAR(255),
                    ip VARCHAR(255),
                    auto VARCHAR(255),
                    auto_modelo VARCHAR(255),
                    auto_tipo VARCHAR(255),
                    auto_color VARCHAR(255),
                    cantidad_compras_realizadas INT,
                    avatar VARCHAR(255),
                    fec_birthday DATETIME)''')
