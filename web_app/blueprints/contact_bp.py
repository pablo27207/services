from flask import Blueprint, request, jsonify, current_app
from flask_mail import Message

contact_bp = Blueprint("contact", __name__, url_prefix="/api")


@contact_bp.post("/send-suggestion")
def send_suggestion():
    """
    Enviar sugerencia por email
    ---
    tags: [Contact]
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [nombre, email, entidad, message]
            properties:
              nombre:  { type: string, example: "Juan García" }
              email:   { type: string, example: "juan@ejemplo.com" }
              entidad: { type: string, example: "Universidad Nacional" }
              message: { type: string, example: "Sería útil agregar temperatura superficial del mar." }
    responses:
      200:
        description: Sugerencia enviada correctamente
      400:
        description: Faltan datos obligatorios
      500:
        description: Error al enviar el correo
    """
    data       = request.get_json() or {}
    suggestion = data.get("message", "").strip()
    nombre     = data.get("nombre", "").strip()
    email      = data.get("email", "").strip()
    entidad    = data.get("entidad", "").strip()

    if not all([suggestion, nombre, email, entidad]):
        return jsonify({"status": "error",
                        "message": "Faltan datos obligatorios"}), 400

    try:
        mail = current_app.extensions["mail"]
        msg  = Message(
            subject=f"Sugerencia de {nombre}",
            sender=email,
            recipients=["franco.garcia@conocimiento.gob.ar"],
        )
        msg.body = (
            f"📝 Nueva sugerencia recibida:\n\n"
            f"👤 Nombre: {nombre}\n"
            f"🏢 Entidad: {entidad}\n"
            f"📧 Email: {email}\n\n"
            f"💬 Mensaje:\n{suggestion}"
        )
        mail.send(msg)
        return jsonify({"status": "success",
                        "message": "Sugerencia enviada con éxito"}), 200

    except Exception as e:
        print(f"❌ Error al enviar el correo: {e}")
        return jsonify({"status": "error",
                        "message": "Ocurrió un error al enviar la sugerencia"}), 500