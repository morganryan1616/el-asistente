from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import openai

# Cargar variables de entorno
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Endpoint para recomendaciones
@app.route('/recomendar-carrera', methods=['POST'])
def recomendar_carrera():
    data = request.get_json()

    # Validación de datos
    if not all(k in data for k in ("interests", "skills", "goals")):
        return jsonify({"error": "Faltan datos. Por favor incluye intereses, habilidades y metas."}), 400

    # Prompt personalizado
    prompt = (
        "Eres un asistente académico de la Universidad Interamericana de Panamá. "
        "Recomienda carreras ofrecidas por la universidad para una persona con los siguientes intereses, habilidades y metas:\n\n"
        f"Intereses: {', '.join(data['interests'])}\n"
        f"Habilidades: {', '.join(data['skills'])}\n"
        f"Metas: {', '.join(data['goals'])}\n\n"
        "Devuelve la respuesta en el siguiente formato JSON:\n"
        "{\n"
        "  \"recommended_careers\": [\n"
        "    {\n"
        "      \"name\": \"Nombre de la carrera\",\n"
        "      \"description\": \"Descripción de la carrera\",\n"
        "      \"reasons\": \"Razones por las que es adecuada para el perfil\"\n"
        "    }\n"
        "  ]\n"
        "}"
    )

    try:
        # Llamada al API de OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        respuesta = response.choices[0].message['content']
        return jsonify(eval(respuesta))

    except openai.error.OpenAIError as e:
        return jsonify({"error": f"Error con el API de OpenAI: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

# Ejecutar el servidor
if __name__ == '__main__':
    app.run(debug=True)
