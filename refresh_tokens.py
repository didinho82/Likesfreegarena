import json
import os
import requests
import base64

# Configurações via Variáveis de Ambiente (Segurança)
GITHUB_TOKEN = os.getenv("GH_TOKEN")
REPO_OWNER = "didinho82"
REPO_NAME = "Likesfreegarena"
FILE_PATH = "config/br_config.json"
FILE_PATH_ALT = "br_config.json"

CLIENT_ID = "100067"
CLIENT_SECRET = "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3"
USER_AGENT = "GarenaMSDK/4.0.19P9(SM-S908E; Android 11; en; IN)"

def get_new_token(uid, password_hash):
    url = "https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant"
    data = {
        'uid': str(uid),
        'password': password_hash,
        'response_type': "token",
        'client_type': "2",
        'client_secret': CLIENT_SECRET,
        'client_id': CLIENT_ID
    }
    try:
        r = requests.post(url, data=data, headers={'User-Agent': USER_AGENT}, timeout=15)
        if r.status_code == 200:
            return r.json().get("access_token")
    except Exception as e:
        print(f"Erro ao conectar Garena: {e}")
    return None

def main():
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    
    # 1. Tentar ler o arquivo atual do GitHub
    target_path = FILE_PATH
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{target_path}"
    r = requests.get(url, headers=headers)
    if r.status_code == 404:
        target_path = FILE_PATH_ALT
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{target_path}"
        r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("Arquivo de contas não encontrado no GitHub.")
        return

    file_data = r.json()
    sha = file_data.get("sha")
    contas = json.loads(base64.b64decode(file_data['content']).decode())

    # 2. Renovar cada token
    print(f"Iniciando renovação de {len(contas)} contas...")
    sucessos = 0
    for c in contas:
        novo_token = get_new_token(c['uid'], c['password'])
        if novo_token:
            c['password'] = novo_token
            sucessos += 1
            print(f"[OK] UID {c['uid']} renovado.")
        else:
            print(f"[!] UID {c['uid']} falhou na renovação.")

    # 3. Salvar de volta no GitHub se houve mudanças
    if sucessos > 0:
        new_content = base64.b64encode(json.dumps(contas, indent=4).encode()).decode()
        update_data = {
            "message": "🌙 Scheduled Auto-Refresh Tokens",
            "content": new_content,
            "sha": sha,
            "branch": "main"
        }
        requests.put(url, headers=headers, data=json.dumps(update_data))
        print(f"Sincronização concluída: {sucessos} tokens atualizados.")
    else:
        print("Nenhum token foi atualizado.")

if __name__ == "__main__":
    main()
  
