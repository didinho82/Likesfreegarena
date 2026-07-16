import os
import sys
import json
import logging
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

# Configuração de Logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Adiciona o diretório atual ao path para encontrar os módulos locais
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.utils.crypto_utils import encrypt
    from app.protobuf import like_pb2
except ImportError as e:
    logger.error(f"Erro ao importar módulos locais: {e}")

app = Flask(__name__)
CORS(app)

@app.route('/online/')
def home():
    return jsonify({
        "status": "VIP API Online",
        "server": "Brasil",
        "author": "didomodz"
    }), 200

@app.route('/like', methods=['GET'])
def send_like():
    uid_target = request.args.get('uid')
    
    if not uid_target:
        return jsonify({"error": "UID alvo faltando"}), 400
    
    if not uid_target.isdigit():
        return jsonify({"error": "O UID deve conter apenas números"}), 400

    try:
        # Caminho para o arquivo de contas
        base_path = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_path, 'config', 'br_config.json')
        
        # Tenta carregar de variável de ambiente primeiro (mais seguro)
        # Se não existir, tenta carregar do arquivo local
        accounts_json = os.environ.get('GUEST_ACCOUNTS')
        if accounts_json:
            accounts = json.loads(accounts_json)
        elif os.path.exists(config_path):
            with open(config_path, 'r') as f:
                accounts = json.load(f)
        else:
            return jsonify({"error": "Configuração de contas não encontrada"}), 404

        if not accounts:
            return jsonify({"error": "Nenhuma conta disponível"}), 404

        success_count = 0
        
        for acc in accounts:
            try:
                # Cria a mensagem Protobuf conforme o seu like_pb2.py
                like_msg = like_pb2.like()
                like_msg.uid = int(uid_target)
                like_msg.region = "BR" # Região padrão
                
                # Serializa e Criptografa
                binary_data = like_msg.SerializeToString()
                encrypted_data = encrypt(binary_data)

                # Cabeçalhos simulando o jogo
                headers = {
                    'User-Agent': 'FreeFire/2.100.1 (Android; 13)',
                    'Authorization': f"Bearer {acc['password']}",
                    'Content-Type': 'application/octet-stream',
                    'X-GA': 'BR',
                    'Connection': 'Keep-Alive'
                }

                url = "https://client.br.freefiremobile.com/api/v1/profile/like"
                
                # Envia a requisição POST para a Garena
                response = requests.post(url, data=encrypted_data, headers=headers, timeout=8)
                
                if response.status_code == 200:
                    success_count += 1
                
            except Exception as inner_e:
                logger.error(f"Erro na conta {acc.get('uid')}: {inner_e}")
                continue

        return jsonify({
            "status": 200,
            "likes_enviados": success_count,
            "total_contas_usadas": len(accounts)
        }), 200

    except Exception as e:
        logger.exception("Erro interno na API")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
    
