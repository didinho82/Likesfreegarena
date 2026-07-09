from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os
from app.utils.crypto_utils import encrypt
from app.protobuf import like_pb2

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"status": "VIP API Online", "server": "Brasil"}), 200

@app.route('/like', methods=['GET'])
def send_like():
    uid_target = request.args.get('uid')
    if not uid_target:
        return jsonify({"error": "UID alvo faltando"}), 400

    try:
        # Carrega suas contas do br_config.json
        with open('config/br_config.json', 'r') as f:
            accounts = json.load(f)

        success_count = 0
        for acc in accounts:
            # Prepara o pacote Protobuf real
            like_request = like_pb2.LikeProfile()
            like_request.target_uid = int(uid_target)
            like_request.source_uid = int(acc['uid'])
            
            # Criptografa os dados
            binary_data = like_request.SerializeToString()
            encrypted_data = encrypt(binary_data)

            # Envia para o servidor da Garena (Endpoint real)
            headers = {
                'User-Agent': 'FreeFire/2.100.1 (Android; 13)',
                'Authorization': f"Bearer {acc['password']}",
                'Content-Type': 'application/octet-stream'
            }
            
            url = "https://client.br.freefiremobile.com/api/v1/profile/like"
            res = requests.post(url, data=encrypted_data, headers=headers, timeout=10)
            
            if res.status_code == 200:
                success_count += 1

        return jsonify({"status": 200, "likes_enviados": success_count}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
