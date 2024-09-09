import json
from flask import Flask, request, jsonify
import time
import threading
import requests

app = Flask(__name__)

# Función para cargar el contenido de un archivo JSON
def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

# Cargar los archivos JSON
main_menu = load_json('main_menu.json')
sucursal_menu = load_json('sucursal_menu.json')
sucursal_responses = load_json('sucursal_responses.json')
general_responses = load_json('general_responses.json')
main_menu_responses = load_json('main_menu_responses.json')

# Lista de números de teléfono permitidos (sin @c.us)
allowed_numbers = [
    "18494731948@c.us",
    "18498168140@c.us",
    "18299011157@c.us"
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
        send_message(user_id, general_responses['session_close'])

# Función para manejar las respuestas del menú de sucursales
def handle_location_response(user_id, message):
    if message == "8":  # Opción 8: Volver al menú principal
        send_main_menu(user_id)  # Mostrar el menú principal
        sessions[user_id]['awaiting_location_response'] = False  # Dejar de esperar respuestas del menú de sucursales

    elif message in sucursal_responses:
        send_message(user_id, sucursal_responses[message]['response'])

        # Después de 2 segundos, enviar el mensaje para volver al menú principal o cerrar sesión
        time.sleep(2)
        send_message(user_id, general_responses['return_menu_or_close'])
        sessions[user_id]['awaiting_secondary_response'] = True  # Esperar la respuesta para volver al menú o cerrar sesión
        sessions[user_id]['awaiting_location_response'] = False  # Ya no espera una respuesta del menú de sucursales

    else:
        # Si la respuesta es inválida, el sistema sigue esperando una respuesta válida del menú de sucursales
        send_message(user_id, "Lo siento, no entendí esa respuesta. Por favor, intente de nuevo.")
        # Mantener la sesión en estado de espera por una respuesta del menú de sucursales
        sessions[user_id]['awaiting_location_response'] = True


# Función para mostrar el menú de sucursales con la opción de volver al menú principal
def send_location_menu(user_id):
    send_message(user_id, sucursal_menu['sucursal_menu_message'])

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
        return jsonify({"status": "response sent"})  # Mantener el estado activo hasta recibir una respuesta válida

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
            send_message(user_id, general_responses['session_close'])
        else:
            send_message(user_id, "Lo siento, no entendí esa respuesta. Por favor, intente de nuevo.")
        return jsonify({"status": "response sent"})

    # Manejando las respuestas del menú principal
    if message in main_menu_responses:
        # Enviar la respuesta correspondiente una sola vez
        send_message(user_id, main_menu_responses[message]['response'])

        # Después de 2 segundos, enviar opciones para volver al menú principal o cerrar sesión
        time.sleep(2)
        send_message(user_id, general_responses['return_menu_or_close'])
        sessions[user_id]['awaiting_secondary_response'] = True  # Esperar la respuesta para volver al menú o cerrar sesión
        return jsonify({"status": "response sent"})
    
    elif message == "6":
        send_location_menu(user_id)  # Mostrar menú de sucursales
        sessions[user_id]['awaiting_location_response'] = True  # Activar estado de menú de sucursales
        return jsonify({"status": "location menu sent"})
    
    else:
        send_message(user_id, "Lo siento, no entendí esa respuesta. Por favor, intente de nuevo.")
        return jsonify({"status": "invalid response"})

# Función para enviar el menú principal
def send_main_menu(user_id):
    send_message(user_id, main_menu['main_menu_message'])

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
