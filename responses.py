# responses.py

# Menús y mensajes principales
MAIN_MENU = """
¡Hola, querido paciente! 😊
Te estás comunicando con *Pss Odonto-Dom*. Este número está destinado solo para enviar notificaciones. 
Para ayudarte mejor, por favor elige una opción escribiendo el número correspondiente:

1️⃣ *Solicitar cita* 🗓️ 
2️⃣ *Diferencia en mi recibo de pago* 💸 
3️⃣ *Recibo mensajes de otra persona* 🙋 
4️⃣ *No deseo recibir notificaciones* 🚫 
5️⃣ *Contactar al área administrativa* 📞 
6️⃣ *Ver horarios y ubicaciones* 🕒📍
7️⃣ *Soy Odontólogo* 🦷
"""

# Menú para los odontólogos
DENTIST_MENU = """
Estas opciones son para los odontólogos:

1. Quiero aclarar algo de mi Agenda.
2. Necesito confirmar algo acerca de la Facturación y/o Pago.
"""

# Respuestas para las opciones de los odontólogos
DENTIST_RESPONSE_1 = "Favor contactar a la encargada de Call Center Margarita Rosado al Numero de Whatsapp 829-520-4648."
DENTIST_RESPONSE_2 = "Favor comunicarse con la Dra. Nairovis al 829-278-6055 y/o Jajaira Bodden al 849-816-8105."


LOCATION_MENU = """
Estas son nuestras sucursales:

1️⃣ Odonto-Dom Paraíso 🏥
2️⃣ Odonto-Dom Ozama 🏥
3️⃣ Odonto-Dom Herrera 🏥
4️⃣ Odonto-Dom Los Alcarrizos 🏥
5️⃣ Odonto-Dom Villa Mella 🏥
6️⃣ Odonto-Dom San Cristóbal 🏥
7️⃣ Odonto-Dom San Isidro 🏥
8️⃣ Volver al menú principal 🔙

Por favor, elige una sucursal para obtener más información o regresa al menú principal.
"""

BRANCH_INFO = {
    "1": """
📍 *Odonto-Dom Paraíso* 🏥
🕑 *Horario*: 
Lunes a Viernes de 8:00 AM a 5:00 PM

📞 *Contacto*: 
(809) 541-2840 Ext. 1111/ 1112/ 1113/ 1114/ 1115

💬 *WhatsApp*: 
[Haz clic aquí para escribirnos](https://wa.link/82x52b)

📍 *Ubicación*: 
Calle Haim Lopez Penha no. 32

🌍 [Ver en Google Maps](https://maps.app.goo.gl/Jz3ct6BJ35L5juqT9)
    """,
    
    "2": """
📍 *Odonto-Dom Ozama* 🏥
🕑 *Horario*: 
Lunes a Viernes de 8:00 AM a 5:00 PM

📞 *Contacto*: 
(809) 541-2840 Ext. 3221/ 3222

💬 *WhatsApp*: 
[Haz clic aquí para escribirnos](https://wa.link/rr1nu8)

📍 *Ubicación*: 
Av. Venezuela, Local no. 46, Casi Esq. Club de Leones

🌍 [Ver en Google Maps](https://maps.app.goo.gl/Jb9eFghDchacYzTA8)
    """,

    "3": """
📍 *Odonto-Dom Herrera* 🏥
🕑 *Horario*: 
Lunes a Viernes de 8:00 AM a 5:00 PM

📞 *Contacto*: 
(809) 541-2840 Ext. 2201/ 2202

💬 *WhatsApp*: 
[Haz clic aquí para escribirnos](https://wa.link/0t2m2y)

📍 *Ubicación*: 
Av. Isabel Aguiar , Plaza Isabel Aguiar Local No.48, 2do Nivel

🌍 [Ver en Google Maps](https://maps.app.goo.gl/ge78ffrXCs42fCD6A)
    """,

    "4": """
📍 *Odonto-Dom Los Alcarrizos* 🏥
🕑 *Horario*: 
Lunes a Viernes de 8:00 AM a 5:00 PM

📞 *Contacto*: 
(809) 541-2840 Ext.2801/ 2802

💬 *WhatsApp*: 
[Haz clic aquí para escribirnos](https://wa.link/zqe1ec)

📍 *Ubicación*: 
Calle Duarte, Local no. 41, Sector Savica, Al lado del Coliseo Gallístico

🌍 [Ver en Google Maps](https://maps.app.goo.gl/GN1eG8MnEZSJt7Ux5)
    """,

    "5": """
📍 *Odonto-Dom Villa Mella* 🏥
🕑 *Horario*: 
Lunes a Viernes de 8:00 AM a 5:00 PM

📞 *Contacto*: 
(809) 541-2840 Ext. 2501/ 2502

💬 *WhatsApp*: 
[Haz clic aquí para escribirnos](https://wa.link/ydl4h5)

📍 *Ubicación*: 
Av. Hermanas Mirabal, Plaza Galerias Villa Mella, Local No. 762, 1er Nivel

🌍 [Ver en Google Maps](https://maps.app.goo.gl/3TrvBoqbiSQ3NNrX7)
    """,

    "6": """
📍 *Odonto-Dom San Cristobal* 🏥
🕑 *Horario*: 
Lunes a Viernes de 8:00 AM a 5:00 PM

📞 *Contacto*: 
(809) 541-2840 Ext. 2303/ 2304

💬 *WhatsApp*: 
[Haz clic aquí para escribirnos](https://wa.link/haw2r6)

📍 *Ubicación*: 
Calle Padre Ayala, No. 97, Frente al Parque Central Cristobal Colon

🌍 [Ver en Google Maps](https://maps.app.goo.gl/HyHzCYCX341Fehbg8)
    """,

    "7": """
📍 *Odonto-Dom San Isidro* 🏥
🕑 *Horario*: 
Lunes a Viernes de 8:00 AM a 5:00 PM

📞 *Contacto*: 
(809) 541-2840 Ext. 2001/ 2002

💬 *WhatsApp*: 
[Haz clic aquí para escribirnos](https://wa.link/xn749g)

📍 *Ubicación*: 
Calle E, Esquina Calle Z, Brisa Oriental II, Al Lado del Residencial San Jeronimo V

🌍 [Ver en Google Maps](https://maps.app.goo.gl/nVXNVxdgmWhsu7ot8)
    """,
}



FOLLOWUP_MENU = """
Esperamos que la información le haya resultado útil. Puede indicar una respuesta:
1. Volver al menú principal
2. Cerrar sesión
"""

CLOSE_SESSION_MESSAGE = "Sesión cerrada por inactividad."

WRONG_NUMBER_NOTIFICATION = """
Disculpe los inconvenientes causados, en un promedio de 30 días ya no estará recibiendo mensajes.
"""

OPT_OUT_MESSAGE = """
Hemos registrado su solicitud de no recibir notificaciones. Gracias por su paciencia.
"""

CONTACT_INFO_MESSAGE = "Por favor, comuníquese al número 809-541-2840."

# Respuestas nuevas para opciones 1, 2, y respuestas inválidas
REQUEST_APPOINTMENT = "Estimado paciente para solicitar su cita, por favor escribir al número de WhatsApp 829-520-4648."
BILLING_ISSUE = "Estimado paciente, por favor comunicarse con la Arq. Hanny Rodriguez (http://wa.link/mtgpw7) y explicar su caso."
INVALID_RESPONSE = "⚠️ Lo siento, no entendí esa respuesta. Por favor, intente de nuevo."

# Notificaciones a los administradores
NOTIFY_WRONG_NUMBER = "Este número de WhatsApp: {number} indica que le están llegando mensajes incorrectos."
NOTIFY_OPT_OUT = "Este número de WhatsApp: {number} ha solicitado no recibir notificaciones."
