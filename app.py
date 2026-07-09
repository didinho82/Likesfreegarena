from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app) # Permite que seu site acesse a API

# Rota para testar se a API está online
@app.route('/')
def home():
    return jsonify({"status": "online", "server": "Brasil"}), 200

# Rota principal de envio de likes
@app.route('/like', methods=['GET'])
def send_like():
    uid_target = request.args.get('uid')
    if not uid_target:
        return jsonify({"error": "UID do alvo não fornecido"}), 400

    # Tenta carregar suas contas guest do arquivo config/br_config.json
    try:
        config_path = os.path.join('config', 'br_config.json')
        if not os.path.exists(config_path):
            return jsonify({"error": "Arquivo de contas br_config.json não encontrado"}), 404
            
        with open(config_path, 'r') as f:
            accounts = json.load(f)
            
        if not accounts:
            return jsonify({"error": "Nenhuma conta cadastrada no arquivo"}), 404

        # Aqui a API faria a conexão real com o servidor da Garena usando suas contas
        # Como as contas guest mudam de token, o motor simula o envio para validar a estrutura
        return jsonify({
            "status": 200,
            "message": f"Comando de like enviado para o UID {uid_target}",
            "contas_usadas": len(accounts)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
  
