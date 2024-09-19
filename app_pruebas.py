from flask import Flask, request, jsonify
import time
import threading
import requests
import responses  # Importamos el archivo de respuestas

app = Flask(__name__)

# Lista de números de teléfono permitidos
allowed_numbers = ["18494731948@c.us", "18498168140@c.us", "18299011157@c.us", "18296784895@c.us"]

class SessionManager:
    def __init__(self):
        self.sessions = {}

    def start_session(self, user_id):
        self.sessions[user_id] = {
            'active': True,
            'awaiting_location_response': False,
            'awaiting_secondary_response': False,
            'awaiting_dentist_menu_response': False
        }
        threading.Thread(target=self.auto_close_session, args=(user_id,)).start()

    def close_session(self, user_id):
        if user_id in self.sessions:
            self.sessions[user_id]['active'] = False
            send_message(user_id, responses.CLOSE_SESSION_MESSAGE)
            # Eliminar la sesión para garantizar que no quede activa
            del self.sessions[user_id]

    def auto_close_session(self, user_id):
        time.sleep(300)
        self.close_session(user_id)

    def is_active(self, user_id):
        return self.sessions.get(user_id, {}).get('active', False)

    def set_awaiting_location_response(self, user_id, status):
        if user_id in self.sessions:
            self.sessions[user_id]['awaiting_location_response'] = status

    def set_awaiting_secondary_response(self, user_id, status):
        if user_id in self.sessions:
            self.sessions[user_id]['awaiting_secondary_response'] = status

    def set_awaiting_dentist_menu_response(self, user_id, status):
        if user_id in self.sessions:
            self.sessions[user_id]['awaiting_dentist_menu_response'] = status

    def is_awaiting_location_response(self, user_id):
        return self.sessions.get(user_id, {}).get('awaiting_location_response', False)

    def is_awaiting_secondary_response(self, user_id):
        return self.sessions.get(user_id, {}).get('awaiting_secondary_response', False)

    def is_awaiting_dentist_menu_response(self, user_id):
        return self.sessions.get(user_id, {}).get('awaiting_dentist_menu_response', False)

session_manager = SessionManager()

# Función para enviar mensajes utilizando UltraMsg API
def send_message(to, message):
    url = "https://api.ultramsg.com/instance85787/messages/chat"
    payload = {
        "token": "uoivjol0zsvvqms0",
        "to": to,
        "body": message
    }
    headers = {"Content-Type": "application/json"}
    requests.post(url, json=payload, headers=headers)

# Funciones de menú
def send_main_menu(user_id):
    send_message(user_id, responses.MAIN_MENU)

def send_location_menu(user_id):
    send_message(user_id, responses.LOCATION_MENU)

# Respuestas específicas del menú de odontólogo
def handle_dentist_menu_response(user_id, message):
    if message == "1":
        send_message(user_id, responses.DENTIST_RESPONSE_1)
    elif message == "2":
        send_message(user_id, responses.DENTIST_RESPONSE_2)
    else:
        send_invalid_response(user_id)
        send_message(user_id, responses.DENTIST_MENU)  # Volver a mostrar el menú de odontólogos
        session_manager.set_awaiting_dentist_menu_response(user_id, True)  # Seguir esperando respuesta del submenú
        return

    # Después de mostrar la respuesta, enviar opciones para volver al menú o cerrar sesión
    time.sleep(2)
    send_message(user_id, responses.FOLLOWUP_MENU)
    # Aseguramos que pase a esperar una respuesta del menú de "Volver al menú principal" o "Cerrar sesión"
    session_manager.set_awaiting_dentist_menu_response(user_id, False)  # No esperar más del menú de odontólogos
    session_manager.set_awaiting_secondary_response(user_id, True)  # Ahora espera volver/cerrar sesión

# Respuestas específicas para cada sucursal
def handle_location_response(user_id, message):
    if message in responses.BRANCH_INFO:
        send_message(user_id, responses.BRANCH_INFO[message])
        # Luego de mostrar la información de la sucursal, cambiar a esperar respuesta de "Volver" o "Cerrar sesión"
        time.sleep(2)
        send_message(user_id, responses.FOLLOWUP_MENU)
        session_manager.set_awaiting_location_response(user_id, False)  # Ya no espera respuesta del menú de sucursales
        session_manager.set_awaiting_secondary_response(user_id, True)  # Ahora espera una respuesta del menú de volver/cerrar sesión
        return
    elif message == "8":
        send_main_menu(user_id)  # Volver al menú principal
        session_manager.set_awaiting_location_response(user_id, False)
        return
    else:
        send_message(user_id, responses.INVALID_RESPONSE)
        # Mantener en el contexto del menú de sucursales
        send_location_menu(user_id)
        session_manager.set_awaiting_location_response(user_id, True)  # Seguir esperando una respuesta de sucursal
        return

# Manejo de la respuesta del menú principal
def handle_menu_response(user_id, message):
    if message == "1":
        send_message(user_id, responses.REQUEST_APPOINTMENT)
    elif message == "2":
        send_message(user_id, responses.BILLING_ISSUE)
    elif message == "3":
        send_message(user_id, responses.WRONG_NUMBER_NOTIFICATION)
        notify_admins_wrong_number(user_id)
    elif message == "4":
        send_message(user_id, responses.OPT_OUT_MESSAGE)
        notify_admins_opt_out(user_id)
    elif message == "5":
        send_message(user_id, responses.CONTACT_INFO_MESSAGE)
    elif message == "6":
        send_location_menu(user_id)
        session_manager.set_awaiting_location_response(user_id, True)
        return
    elif message == "7":  # Nueva opción: Soy Odontólogo
        send_message(user_id, responses.DENTIST_MENU)
        session_manager.set_awaiting_secondary_response(user_id, False)  # No espera respuesta de volver/cerrar sesión
        session_manager.set_awaiting_dentist_menu_response(user_id, True)  # Esperar respuestas del submenú de odontólogos
        return
    else:
        send_invalid_response(user_id)
        return

    # Después de manejar la respuesta principal, enviar opciones para volver al menú o cerrar sesión
    time.sleep(2)
    send_message(user_id, responses.FOLLOWUP_MENU)
    session_manager.set_awaiting_secondary_response(user_id, True)

def send_invalid_response(user_id):
    send_message(user_id, responses.INVALID_RESPONSE)

# Funciones de notificación a los administradores
def notify_admins_wrong_number(user_number):
    admin_numbers = ["8494731948", "498168140", "299011157"]
    clean_number = user_number.split('@')[0]
    message = responses.NOTIFY_WRONG_NUMBER.format(number=clean_number)
    for admin in admin_numbers:
        send_message(admin, message)

def notify_admins_opt_out(user_number):
    admin_numbers = ["8494731948", "498168140", "299011157"]
    clean_number = user_number.split('@')[0]
    message = responses.NOTIFY_OPT_OUT.format(number=clean_number)
    for admin in admin_numbers:
        send_message(admin, message)

# Webhook para recibir mensajes entrantes y manejar el flujo
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    message_data = data.get('data', {})
    user_id = message_data.get('from')
    message = message_data.get('body').strip()

    if not user_id or not message:
        return jsonify({"error": "Datos no válidos recibidos"}), 400

    if user_id not in allowed_numbers:
        return jsonify({"status": "number not allowed"}), 403

    # Si el usuario está en el menú de sucursales, manejar las respuestas en ese contexto
    if session_manager.is_awaiting_location_response(user_id):
        handle_location_response(user_id, message)
        return jsonify({"status": "response sent"})

    # Manejar las respuestas del submenú de odontólogos
    if session_manager.is_awaiting_dentist_menu_response(user_id):
        handle_dentist_menu_response(user_id, message)
        return jsonify({"status": "response sent"})

    # Manejar las respuestas de "Volver al menú principal" o "Cerrar sesión"
    if session_manager.is_awaiting_secondary_response(user_id):
        if message == "1":
            send_main_menu(user_id)
            session_manager.set_awaiting_secondary_response(user_id, False)
        elif message == "2":
            session_manager.close_session(user_id)
            return jsonify({"status": "session closed"})  # Aquí marcamos que la sesión está cerrada
        else:
            send_invalid_response(user_id)
        return jsonify({"status": "response sent"})

    if not session_manager.is_active(user_id):
        session_manager.start_session(user_id)
        send_main_menu(user_id)
        return jsonify({"status": "session started"})

    handle_menu_response(user_id, message)
    return jsonify({"status": "response sent"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
