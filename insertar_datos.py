import sys
import requests
import mysql.connector
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from base64 import b64encode

# Consumir el servidor del proveedor
usuarios = requests.get("https://62433a7fd126926d0c5d296b.mockapi.io/api/v1/usuarios")

# Obtener llave para cifrar los datos, por practicidad se guarda la llave acá
external_key = b'\xe5\x8aXg\x18\xa5y\x15\x1f\xa49\xaa\xf1\xf7\x9d\xcc\x96\xba\xc5\xfe\xf2\x93O\x82\x90{G\x80\x1c&\xa5Y'

# Inicializar el objeto cipher que utiliza la libreria AES junto con la llave obtenida y modelo CBC para cifrar los datos
cipher = AES.new(external_key, AES.MODE_CBC)
iv = cipher.iv

# Conectar a la base de datos
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="usermanager",
    password="hcO/rG0HsJLv+dXv",
    database="repositorio"
)


# Crear un cursor para ejecutar las acciones en la base de datos
cursor = conn.cursor()

# Recorrer todos los usuarios para cargarlos a la Base de datos
for usuario in usuarios.json():
    # Se cifran los datos de la tarjeta
    data = bytes(usuario['credit_card_num'], 'utf-8')
    padded_data = pad(data, AES.block_size)
    cipher_text = cipher.encrypt(padded_data)
    encoded_cipher_text = b64encode(cipher_text)
    usuario['credit_card_num'] = encoded_cipher_text

    # Se cifran el ccv de la tarjeta
    data = bytes(usuario['credit_card_ccv'], 'utf-8')
    padded_data = pad(data, AES.block_size)
    cipher_text = cipher.encrypt(padded_data)
    encoded_cipher_text = b64encode(cipher_text)
    usuario['credit_card_ccv'] = encoded_cipher_text

    # Si las fechas no se pasan a este formato, genera error: Incorrect datetime value: '2021-07-31T00:11:06.741Z' for column 'fec_alta' at row 1
    usuario['fec_alta'] = datetime.fromisoformat(usuario['fec_alta'].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')
    usuario['fec_birthday'] = datetime.fromisoformat(usuario['fec_birthday'].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')

    sql = '''INSERT INTO usuarios (fec_alta, user_name, codigo_zip, credit_card_num, credit_card_ccv, 
            cuenta_numero, direccion, geo_latitud, geo_longitud, color_favorito, foto_dni, ip, 
            auto, auto_modelo, auto_tipo, auto_color, cantidad_compras_realizadas, avatar, fec_birthday) 
            VALUES (%(fec_alta)s, %(user_name)s, %(codigo_zip)s, %(credit_card_num)s, %(credit_card_ccv)s, 
            %(cuenta_numero)s, %(direccion)s, %(geo_latitud)s, %(geo_longitud)s, %(color_favorito)s, %(foto_dni)s, 
            %(ip)s, %(auto)s, %(auto_modelo)s, %(auto_tipo)s, %(auto_color)s, %(cantidad_compras_realizadas)s, 
            %(avatar)s, %(fec_birthday)s)'''

    # Intentar guardar la información del usuario en la base de datos
    try:
        cursor.execute(sql, usuario)
    except Exception as e:
        print("Error inserting: ", e)
        sys.exit(1)

    # Guardar los cambios en la base de datos
    conn.commit()


# Cerrar la conexión
conn.close()

print("Los datos se han guardado exitosamente en la base de datos.")
