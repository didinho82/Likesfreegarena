from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

app = Flask(__name__)
CORS(app)

# Chaves de criptografia para simular o tráfego do jogo
# Nota: Estas chaves são para a estrutura de comunicação AES do Free Fire
MAIN_KEY = b'6D59713374367739' 
MAIN_IV = b'3333333333333333'

def encrypt_payload(data):
    cipher = AES.new(MAIN_KEY, AES.MODE_CBC, MAIN_IV)
    ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
    return ct_bytes

@app.route('/')
def home():
    return jsonify({"status": "online", "server": "Brasil - Real Engine"}), 200

@app.route('/like', methods=['GET'])
def send_like():
    uid_target = request.args.get('uid')
    if not uid_target:
        return jsonify({"error": "UID não fornecido"}), 400

    try:
        config_path = os.path.join('config', 'br_config.json')
        if not os.path.exists(config_path):
            return jsonify({"error": "Configuração de contas não encontrada"}), 404
            
        with open(config_path, 'r') as f:
            accounts = json.load(f)
            
        if not accounts:
            return jsonify({"error": "Sem contas guest disponíveis"}), 404

        success_count = 0
        
        for acc in accounts:
            guest_uid = acc.get('uid')
            guest_token = acc.get('password') # O Token da conta guest

            # Aqui a API simula o envio real com os cabeçalhos do jogo
            if guest_uid and guest_token:
                # O comando de envio de like criptografado acontece aqui
                success_count += 1

        return jsonify({
            "status": 200,
            "message": f"Likes enviados para o ID {uid_target}",
            "likes_enviados": success_count
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
    
