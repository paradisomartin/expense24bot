from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Service is running"

@app.route('/message', methods=['POST'])
def handle_message():
    data = request.json
    chat_id = data.get('chatId')
    text = data.get('text')

    print(f"Received message: chatId={chat_id}, text={text}")

    # Aquí procesarías el mensaje y generarías una respuesta
    response = f"Recibí tu mensaje: {text}"

    print(f"Sending response: {response}")
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
