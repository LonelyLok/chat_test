from flask import Flask, session, request, jsonify, Response
import os
import google.generativeai as genai
import json
from dotenv import load_dotenv
from flask_cors import CORS
from user_sessions import create_user_sessions, delete_user_session, get_user_sessions_from_user_id, get_user_session, update_user_sessions
from chat_history import delete_chat_history_by_session_id, create_chat_history, get_chat_history_from_session_id
import datetime
import config
api_key = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=api_key)

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5173", "http://localhost:5173", "http://frontend:5173"])

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/chat', methods=['POST'])
def send_message():
    user_input = request.json.get('message')
    session_id = request.json.get('session_id')
    model_name = request.json.get('model')
    print(model_name)

    model = genai.GenerativeModel(model_name)

    history = get_chat_history_from_session_id(session_id)

    history = [{'role': 'user' if his['is_bot'] == False else 'model', 'parts': [{'text': his['message']}]} for his in history]

    chat = model.start_chat(history=history)

    create_chat_history(id=None, session_id=session_id, message=user_input,
                        is_bot=False, timestamp=datetime.datetime.now(datetime.timezone.utc))

    response_generator = chat.send_message(user_input, stream=True)
    # response_text = ''.join([chunk.text for chunk in response])

    response_chunks = []

    def generate():
        for chunk in response_generator:
            # Convert each JSON string to bytes before yielding
            response_chunks.append(chunk.text)
            yield json.dumps({"response": chunk.text}).encode('utf-8') + b"\n"

    response = Response(generate(), mimetype='application/json')

    @response.call_on_close
    def on_close():
        bot_response = ''.join(response_chunks)
        create_chat_history(id=None, session_id=session_id, message=bot_response,
                            is_bot=True, timestamp=datetime.datetime.now(datetime.timezone.utc))
    return response


# @app.route('/chat_history_old', methods=['GET'])
# def get_chat_history_old():
#     session_id = request.args.get('session_id')
#     if not session_id:
#         return jsonify({"error": "Session ID is required"}), 400
#     chat = sessions.get(session_id)
#     if (chat is None):
#         return jsonify({'data': []})
#     return jsonify({'data': chat.history})


@app.route('/chat_history', methods=['GET'])
def get_chat_history():
    session_id = request.args.get('session_id')
    if not session_id:
        return jsonify({"error": "Session ID is required"}), 400
    history = get_chat_history_from_session_id(session_id)
    return jsonify({'data': history})


@app.route('/create_session', methods=['POST'])
def create_chat_session():
    session_id = request.json.get('session_id')
    user_id = request.json.get('user_id')
    if not session_id or not user_id:
        return jsonify({"error": "Session ID and User ID is required"}), 400
    res = create_user_sessions(
        user_id, session_id, created_at=datetime.datetime.now(datetime.timezone.utc), model='models/gemini-1.5-pro-latest')
    return jsonify({'message': 'Session created successfully', 'data': res })


@app.route('/delete_session', methods=['POST'])
def delete_chat_session():
    session_id = request.json.get('session_id')
    user_id = request.json.get('user_id')
    if not session_id or not user_id:
        return jsonify({"error": "Session ID and User ID is required"}), 400
    delete_user_session(user_id, session_id)
    delete_chat_history_by_session_id(session_id)
    return jsonify({'message': 'Session deleted successfully'})


@app.route('/get_user_sessions', methods=['GET'])
def get_user_sessions():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    user_sessions = get_user_sessions_from_user_id(user_id)
    return jsonify({'data': user_sessions})

@app.route('/get_user_session', methods=['GET'])
def fetch_user_session():
    user_id = request.args.get('user_id')
    session_id = request.args.get('session_id')
    if not user_id or not session_id:
        return jsonify({"error": "User ID and Session ID is required"}), 400
    user_session = get_user_session(user_id, session_id)
    return jsonify({'data': user_session})

@app.route('/update_user_session', methods=['POST'])
def update_user_session():
    user_id = request.json.get('user_id')
    session_id = request.json.get('session_id')
    model = request.json.get('model')
    if not user_id or not session_id or not model:
        return jsonify({"error": "User ID, Session ID and Model is required"}), 400
    res = update_user_sessions(user_id, session_id, model)
    return jsonify({'message': 'Session updated successfully', 'data': res })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

    # chat = model.start_chat()
    # response = chat.send_message('hello what is the plan for today?')

    # print(chat.history)
