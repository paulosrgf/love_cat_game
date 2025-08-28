import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import json

# --------------------------
# Configuração do Flask (APENAS UMA VEZ)
# --------------------------
app = Flask(
    __name__,
    static_folder="../front_end",
    template_folder="../front_end"
)
CORS(app)

# Obter o diretório atual do arquivo app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORIA_JSON = os.path.join(BASE_DIR, "historia.json")

# --------------------------
# Funções auxiliares (APENAS UMA VEZ)
# --------------------------

def carregar_historia():
    """Carrega o arquivo historia.json"""
    try:
        with open(HISTORIA_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {HISTORIA_JSON}")
        return {
            "cenas": {
                "inicio": {
                    "id": "inicio",
                    "texto": "Arquivo de história não encontrado.",
                    "opcoes": {},
                    "final": True
                }
            },
            "config": {
                "titulo": "História Padrão",
                "personagem_principal": "Personagem",
                "version": "1.0"
            }
        }
    except json.JSONDecodeError as e:
        print(f"Erro JSON: {e}")
        return {"erro": f"Erro ao decodificar o arquivo JSON: {e}"}

def salvar_historia(dados):
    """Salva dados no arquivo historia.json"""
    try:
        with open(HISTORIA_JSON, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e}")
        return False

# --------------------------
# Rotas da API
# --------------------------

@app.route("/iniciar", methods=["GET"])
def iniciar_jogo():
    print("=== DEBUG: Rota /iniciar chamada ===")
    historia = carregar_historia()
    print(f"DEBUG: História carregada - {historia}")
    
    if "erro" in historia:
        print(f"DEBUG: Erro na história - {historia['erro']}")
        return jsonify({"erro": historia["erro"]}), 500
    
    cena_inicio = historia["cenas"].get("inicio")
    print(f"DEBUG: Cena início - {cena_inicio}")
    
    return jsonify(cena_inicio) if cena_inicio else (jsonify({"erro": "Cena início não encontrada"}), 404)

@app.route("/cena/<cena_id>", methods=["GET"])
def obter_cena(cena_id):
    historia = carregar_historia()
    if "erro" in historia:
        return jsonify({"erro": historia["erro"]}), 500
    
    cena = historia["cenas"].get(cena_id)
    return jsonify(cena) if cena else (jsonify({"erro": "Cena não encontrada."}), 404)

@app.route("/avancar", methods=["POST"])
def avancar_jogo():
    dados = request.json or {}
    escolha = dados.get("escolha")
    cena_atual_id = dados.get("cena_atual", "inicio")

    historia = carregar_historia()
    if "erro" in historia:
        return jsonify({"erro": historia["erro"]}), 500
    
    cena_atual = historia["cenas"].get(cena_atual_id)
    if not cena_atual:
        return jsonify({"erro": "Cena atual não encontrada."}), 404
    
    if not escolha:
        return jsonify(cena_atual)
    
    proxima_cena_id = cena_atual["opcoes"].get(escolha)
    if not proxima_cena_id:
        return jsonify({"erro": "Opção não disponível nesta cena."}), 400
    
    proxima_cena = historia["cenas"].get(proxima_cena_id)
    return jsonify(proxima_cena) if proxima_cena else (jsonify({"erro": "Próxima cena não encontrada."}), 404)

@app.route("/info", methods=["GET"])
def obter_info():
    historia = carregar_historia()
    return jsonify(historia.get("config", {}))

@app.route("/cenas", methods=["GET"])
def listar_cenas():
    historia = carregar_historia()
    return jsonify(historia.get("cenas", {}))

@app.route("/cena", methods=["POST"])
def adicionar_cena():
    nova_cena = request.json
    if not nova_cena or "id" not in nova_cena:
        return jsonify({"erro": "ID da cena é obrigatório"}), 400
        
    historia = carregar_historia()
    if "erro" in historia:
        return jsonify({"erro": historia["erro"]}), 500
        
    historia["cenas"][nova_cena["id"]] = nova_cena

    if salvar_historia(historia):
        return jsonify({"mensagem": "Cena salva com sucesso.", "cena": nova_cena})
    else:
        return jsonify({"erro": "Erro ao salvar cena."}), 500

@app.route("/health", methods=["GET"])
def health_check():
    historia = carregar_historia()
    return jsonify({
        "status": "ativo",
        "total_cenas": len(historia.get("cenas", {})),
        "titulo": historia.get("config", {}).get("titulo", "Desconhecido")
    })

# --------------------------
# Rotas para o Front-End
# --------------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

# --------------------------
# Execução do servidor
# --------------------------

if __name__ == "__main__":
    print("=== Iniciando servidor Flask ===")
    print(f"Diretório atual: {BASE_DIR}")
    print(f"Caminho do JSON: {HISTORIA_JSON}")
    
    # Verificar se o arquivo JSON existe
    if os.path.exists(HISTORIA_JSON):
        print("✓ Arquivo historia.json encontrado")
    else:
        print("✗ Arquivo historia.json NÃO encontrado")
        print("  Certifique-se de que o arquivo está na pasta back_end/")
    
    app.run(host="0.0.0.0", port=5000, debug=True)
    