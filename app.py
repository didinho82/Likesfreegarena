from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os
import sys

# Garante que o Python encontre as pastas locais
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importações corrigidas
try:
    from app.utils.crypto_utils import encrypt
    from app.protobuf import like_pb2
except ImportError as e:
    # Se falhar, tenta importar diretamente (caso a estrutura mude no deploy)
    print(f"Erro de importação: {e}")

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
        # Caminho absoluto para o arquivo de configuração
        base_path = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_path, 'config', 'br_config.json')
        
        if not os.path.exists(config_path):
            return jsonify({"error": "Configuração de contas não encontrada"}), 404
            
        with open(config_path, 'r') as f:
            accounts = json.load(f)

        success_count = 0
        for acc in accounts:
            try:
                # Lógica real de envio usando Protobuf
                like_request = like_pb2.LikeProfile()
                like_request.target_uid = int(uid_target)
                like_request.source_uid = int(acc['uid'])
                
                binary_data = like_request.SerializeToString()
                encrypted_data = encrypt(binary_data)

                headers = {
                    'User-Agent': 'FreeFire/2.100.1 (Android; 13)',
                    'Authorization': f"Bearer {acc['password']}",
                    'Content-Type': 'application/octet-stream'
                }
                
                url = "https://client.br.freefiremobile.com/api/v1/profile/like"
                res = requests.post(url, data=encrypted_data, headers=headers, timeout=10)
                
                if res.status_code == 200:
                    success_count += 1
            except:
                continue # Pula para a próxima conta se uma falhar

        return jsonify({"status": 200, "likes_enviados": success_count}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
    
