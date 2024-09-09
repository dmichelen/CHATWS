from flask import Flask, request, jsonify
import time
import threading
import requests

app = Flask(__name__)

# Lista de números de teléfono permitidos (sin @c.us)
allowed_numbers = [
    "18494731948@c.us",
    "18498168140@c.us",
    "18291157@c.us"
]

# Función para enviar mensajes utilizando UltraMsg API
def send_message(to, message):
    url = "https://api.ultramsg.com/instance85787/messages/chat"
    payload = {
        "token": "uoivjol0zsvvqms0",
        "to": to,
        "body": message
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Mensaje enviado exitosamente.")
    else:
        print("Error al enviar el mensaje:", response.status_code, response.text)

# Diccionario para mantener las sesiones de usuario
sessions = {}

# Función para manejar el cierre automático de sesión
def auto_close_session(user_id):
    time.sleep(300)  # Espera 5 minutos
    if user_id in sessions and sessions[user_id]['active']:
        sessions[user_id]['active'] = False
        send_message(user_id, "Sesión cerrada por inactividad.")

# Función para manejar las respuestas del menú de sucursales
def handle_location_response(user_id, message):
    if message == "1":
        send_message(user_id, """
        📍 *Odonto-Dom Paraíso*
        Horario: Lunes a Viernes de 8:00 AM a 5:00 PM
        Contacto: 809-123-4567
        Ubicación: Av. Winston Churchill, Santo Domingo
        [Ver en Google Maps](https://goo.gl/maps/xyz123)
        """)
    elif message == "2":
        send_message(user_id, """
        📍 *Odonto-Dom Ozama*
        Horario: Lunes a Viernes de 9:00 AM a 6:00 PM
        Contacto: 809-987-6543
        Ubicación: Av. Venezuela, Santo Domingo Este
        [Ver en Google Maps](https://goo.gl/maps/abc456)
        """)
    elif message == "3":
        send_message(user_id, """
        📍 *Odonto-Dom Herrera*
        Horario: Lunes a Viernes de 8:30 AM a 5:30 PM
        Contacto: 809-654-3210
        Ubicación: Av. Isabel Aguiar, Santo Domingo Oeste
        [Ver en Google Maps](https://goo.gl/maps/qwe789)
        """)
    elif message == "4":
        send_message(user_id, """
        📍 *Odonto-Dom Los Alcarrizos*
        Horario: Lunes a Viernes de 9:00 AM a 5:00 PM
        Contacto: 809-123-4321
        Ubicación: Calle Duarte, Los Alcarrizos
        [Ver en Google Maps](https://goo.gl/maps/asd123)
        """)
    elif message == "5":
        send_message(user_id, """
        📍 *Odonto-Dom Villa Mella*
        Horario: Lunes a Viernes de 9:00 AM a 5:30 PM
        Contacto: 809-321-6547
        Ubicación: Av. Hermanas Mirabal, Villa Mella
        [Ver en Google Maps](https://goo.gl/maps/zxc456)
        """)
    elif message == "6":
        send_message(user_id, """
        📍 *Odonto-Dom San Cristóbal*
        Horario: Lunes a Viernes de 8:00 AM a 5:00 PM
        Contacto: 809-789-1234
        Ubicación: Calle Principal, San Cristóbal
        [Ver en Google Maps](https://goo.gl/maps/qwe123)
        """)
    elif message == "7":
        send_message(user_id, """
        📍 *Odonto-Dom San Isidro*
        Horario: Lunes a Viernes de 9:00 AM a 6:00 PM
        Contacto: 809-456-7890
        Ubicación: Carretera Mella, San Isidro
        [Ver en Google Maps](https://goo.gl/maps/rty789)
        """)
    elif message == "8":
        send_main_menu(user_id)  # Volver al menú principal
    else:
        send_message(user_id, "Lo siento, no entendí esa respuesta. Por favor, intente de nuevo.")
        return

    # Después de 2 segundos, enviar el mensaje para volver al menú principal o cerrar sesión
    time.sleep(2)
    send_message(user_id, """
    Esperamos que la información le haya resultado útil. Puede indicar una respuesta:
    1. Volver al menú principal
    2. Cerrar sesión
    """)
    sessions[user_id]['awaiting_secondary_response'] = True  # Esperar la respuesta para volver al menú o cerrar sesión

# Función para mostrar el menú de sucursales con la opción de volver al menú principal
def send_location_menu(user_id):
    send_message(user_id, """
    Estas son nuestras sucursales:

    ① *Odonto-Dom Paraíso* 🏥  
    ② *Odonto-Dom Ozama* 🏥  
    ③ *Odonto-Dom Herrera* 🏥  
    ④ *Odonto-Dom Los Alcarrizos* 🏥  
    ⑤ *Odonto-Dom Villa Mella* 🏥  
    ⑥ *Odonto-Dom San Cristóbal* 🏥  
    ⑦ *Odonto-Dom San Isidro* 🏥  
    ⑧ *Volver al menú principal* 🔙

    Por favor, elige una sucursal para obtener más información o regresa al menú principal.
    """)

# Webhook para recibir mensajes entrantes y manejar el flujo
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Datos recibidos:", data)  # Imprimir los datos recibidos para depuración

    # Acceder a los datos importantes dentro de la clave 'data'
    message_data = data.get('data', {})
    if 'from' not in message_data or 'body' not in message_data:
        return jsonify({"error": "Datos no válidos recibidos"}), 400

    user_id = message_data['from']
    clean_number = user_id.split('@')[0]

    # Verificar si el número está en la lista de números permitidos
    if user_id not in allowed_numbers:
        print(f"Número {user_id} no está en la lista permitida. Ignorando mensaje.")
        return jsonify({"status": "number not allowed"}), 403

    message = message_data['body'].strip()

    # Control de estado: si el usuario está en el menú de sucursales
    if sessions.get(user_id, {}).get('awaiting_location_response'):
        handle_location_response(user_id, message)
        sessions[user_id]['awaiting_location_response'] = False
        return jsonify({"status": "response sent"})

    # Si el usuario inicia una nueva sesión o si está inactiva
    if user_id not in sessions or not sessions[user_id]['active']:
        sessions[user_id] = {'active': True}
        threading.Thread(target=auto_close_session, args=(user_id,)).start()
        send_main_menu(user_id)
        return jsonify({"status": "session started"})

    # Manejo de la respuesta después de mostrar opciones de menú o cerrar sesión
    if sessions[user_id].get('awaiting_secondary_response'):
        if message == "1":
            send_main_menu(user_id)
            sessions[user_id]['awaiting_secondary_response'] = False
        elif message == "2":
            sessions[user_id]['active'] = False
            send_message(user_id, "Sesión cerrada. Gracias por contactarnos.")
        else:
            send_message(user_id, "Lo siento, no entendí esa respuesta. Por favor, intente de nuevo.")
        return jsonify({"status": "response sent"})

    # Manejando las respuestas del menú principal
    if message == "1":
        send_message(user_id, "Estimado paciente para solicitar su cita, por favor escribir al número de WhatsApp 829-520-4648.")
    elif message == "2":
        send_message(user_id, "Estimado paciente, por favor comunicarse al número #### y explicar su caso, confirmando siempre la sucursal donde se atendió.")
    elif message == "3":
        send_message(user_id, "Disculpe los inconvenientes causados, en un promedio de 30 días ya no estará recibiendo mensajes a su número.")
        notify_admins_wrong_number(user_id)
    elif message == "4":
        send_message(user_id, "Hemos registrado su solicitud de no recibir notificaciones por esta vía. Gracias por su paciencia.")
        notify_admins_opt_out(user_id)
    elif message == "5":
        send_message(user_id, "Por favor, comuníquese al número 809-541-2840.")
    elif message == "6":
        send_location_menu(user_id)  # Mostrar menú de sucursales
        sessions[user_id]['awaiting_location_response'] = True  # Activar estado de menú de sucursales
        return jsonify({"status": "location menu sent"})
    else:
        send_message(user_id, "Lo siento, no entendí esa respuesta. Por favor, intente de nuevo.")
        return jsonify({"status": "invalid response"})

    # Después de 2 segundos, enviar opciones para volver al menú o cerrar sesión
    time.sleep(2)
    send_message(user_id, """
    Esperamos que la información le haya resultado útil. Puede indicar una respuesta:
    1. Volver al menú principal
    2. Cerrar sesión
    """)
    sessions[user_id]['awaiting_secondary_response'] = True  # Esperar la respuesta para volver al menú o cerrar sesión

    return jsonify({"status": "response sent"})

# Función para enviar el menú principal
def send_main_menu(user_id):
    send_message(user_id, """
    ¡Hola, querido paciente! 😊

    Te estás comunicando con *Pss Odonto-Dom*. Este número está destinado solo para enviar notificaciones.  
    Para ayudarte mejor, por favor elige una opción escribiendo el número correspondiente:

    ① *Solicitar cita* 🗓️  
    ② *Tengo una diferencia en mi recibo de pago* 💸  
    ③ *Estoy recibiendo mensajes de otra persona* 🙋  
    ④ *No deseo recibir notificaciones de ningún tipo* 🚫  
    ⑤ *Contactar al área administrativa* 📞  
    ⑥ *Ver horarios y ubicaciones* 🕒📍
    """)

# Funciones de notificación a los administradores
def notify_admins_wrong_number(user_number):
    admin_numbers = ["8494731948", "8498168140", "8299011157"]
    clean_number = user_number.split('@')[0]
    message = f"Este número de WhatsApp: {clean_number} indica que le están llegando mensajes que no le pertenecen, por favor verificar para solucionar este caso. Muchas gracias."
    for admin in admin_numbers:
        send_message(admin, message)

def notify_admins_opt_out(user_number):
    admin_numbers = ["8494731948", "8498168140", "8299011157"]
    clean_number = user_number.split('@')[0]
    message = f"Este número de WhatsApp: {clean_number} ha solicitado no recibir notificaciones por esta vía. El número es correcto, pero el usuario desea darse de baja. Por favor, procedan con la solicitud."
    for admin in admin_numbers:
        send_message(admin, message)

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
