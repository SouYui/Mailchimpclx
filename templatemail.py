import os
from flask import Flask, request, jsonify
from mailchimp_transactional import Client
from mailchimp_transactional.api_client import ApiClientError
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env (para entornos locales)
load_dotenv()

app = Flask(__name__)

# Obtener la clave API desde las variables de entorno
MAILCHIMP_API_KEY = os.getenv("MAILCHIMP_API_KEY")

@app.route('/enviar-template', methods=['POST'])
def enviar_template():
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()
        
        # Validar parámetros requeridos
        if not data or not all(key in data for key in ["template_name", "template_content", "message"]):
            return jsonify({"codigo": 1, "error": "Faltan parámetros requeridos"}), 400

        # Inicializar el cliente de MailChimp con la clave API
        mailchimp = Client(MAILCHIMP_API_KEY)

        # Enviar correo utilizando un template
        response = mailchimp.messages.send_template({
            "template_name": data["template_name"],
            "template_content": data["template_content"],
            "message": data["message"]
        })

        # Respuesta exitosa
        return jsonify({"codigo": 0, "mensaje": "Correo enviado exitosamente", "response": response})

    except ApiClientError as error:
        # Error específico de la API de MailChimp
        return jsonify({"codigo": 2, "error": error.text}), 500

    except Exception as e:
        # Cualquier otro error
        return jsonify({"codigo": 3, "error": str(e)}), 500

if __name__ == '__main__':
    # Obtener el puerto desde las variables de entorno o usar 5000 por defecto
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
