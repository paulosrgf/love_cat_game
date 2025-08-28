from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

# carregar historia do json
def carregar_historia():
    try:
        with open('historia.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # retorna uma historia padrão se o arquivo não for encontrado
        return {
            "cenas": {
                "inicio": {
                    "id": "inicio",
                    "texto": "Arquivo de historia nao encontrado.",
                    "opcoes": {},
                    "final": True
                }
            },
            "config": {
                "titulo": "Historia Padrão",
                "personagem_principal": "personagem",
                "version": "1.0"
            }
        }
    except json.JSONDecodeError:
        return {"erro": "Erro ao decodificar o arquivo JSON."}

# Salvar historia no JSON
def salvar_historia(dados):
    try:
        with open('historia.json', 'w', encoding='utf-8') as f:  # Corrigido: 'history.json' → 'historia.json'
            json.dump(dados, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e}")
        return False

# Rotas da API (iniciar o jogo)
@app.route('/iniciar', methods=['GET'])
def iniciar_jogo():
    historia = carregar_historia()  # Corrigido: faltou os parênteses ()
    if "erro" in historia:
        return jsonify({"erro": historia["erro"]}), 500
    
    return jsonify(historia["cenas"]["inicio"])

# Rota para obter uma cena especifica
@app.route('/cena/<cena_id>', methods=['GET'])
def obter_cena(cena_id):
    historia = carregar_historia()
    if "erro" in historia:
        return jsonify({"erro": historia["erro"]}), 500
    
    cena = historia["cenas"].get(cena_id)
    if cena:
        return jsonify(cena)
    else:
        return jsonify({"erro": "Cena nao encontrada."}), 404

# rotas para avançar no jogo
@app.route('/avancar', methods=['POST'])
def avancar_jogo():
    dados = request.json
    escolha = dados.get("escolha")
    cena_atual_id = dados.get("cena_atual", "inicio")

    historia = carregar_historia()
    if "erro" in historia:
        return jsonify({"erro": historia["erro"]}), 500
    
    # Verifica se a cena atual existe
    cena_atual = historia["cenas"].get(cena_atual_id)  # Corrigido: buscar a cena atual do JSON
    if not cena_atual:
        return jsonify({"erro": "Cena atual não encontrada."}), 404
    
    # Se não houver escolha, retorna a cena atual
    if not escolha:
        return jsonify(cena_atual)  # Corrigido: retornar cena_atual, não cena_atual_id
    
    # Obtém a proxima cena com base na escolha
    proxima_cena_id = cena_atual["opcoes"].get(escolha)  # Corrigido: usar cena_atual, não cena_atual_id

    if not proxima_cena_id:
        return jsonify({"erro": "Opção não disponível nesta cena."}), 400  # Corrigido: erro 400, não 404
    
    proxima_cena = historia["cenas"].get(proxima_cena_id)

    if proxima_cena:
        return jsonify(proxima_cena)
    else:
        return jsonify({"erro": "Próxima cena não encontrada."}), 404

# Rota para obter informações do jogo
@app.route('/info', methods=['GET'])
def obter_info():
    historia = carregar_historia()
    if "erro" in historia:
        return jsonify({"erro": historia["erro"]}), 500   
        
    return jsonify(historia["config"])

# Rota para listar todas as cenas (util para debug)
@app.route('/cenas', methods=['GET'])
def listar_cenas():
    historia = carregar_historia()
    if "erro" in historia:
        return jsonify({"erro": historia["erro"]}), 500 
    return jsonify(historia["cenas"])

# Rota para adicionar/atualizar uma cena (apenas para desenvolvimento)
@app.route('/cena', methods=['POST'])
def adicionar_cena():
    nova_cena = request.json

    if not nova_cena or "id" not in nova_cena:
        return jsonify({"erro": "ID da cena é obrigatório"}), 400
        
    historia = carregar_historia()
    if "erro" in historia:
        return jsonify({"erro": historia["erro"]}), 500
        
    historia["cenas"][nova_cena["id"]] = nova_cena  # Corrigido: "cena" → "cenas"

    if salvar_historia(historia):
        return jsonify({"mensagem": "Cena salva com sucesso.", "cena": nova_cena})
    else:
        return jsonify({"erro": "Erro ao salvar cena."}), 500

# Rota de health check
@app.route('/health', methods=['GET'])
def health_check():
    historia = carregar_historia()
    if "erro" in historia: 
        return jsonify({"status": "ativo", "historia": "erro ao carregar"})
            
    return jsonify({
        "status": "ativo",
        "total_cenas": len(historia["cenas"]),
        "titulo": historia["config"]["titulo"]
    })

@app.route("/")
def home():
    return "Página home - API do Jogo de Aventura Textual"

# Parte do servidor - CORRIGIDA (removido código duplicado)
if __name__ == "__main__":
    # Verifica se o arquivo de história existe, se não, cria um com a estrutura básica
    if not os.path.exists('historia.json'):
        historia_base = {
            "cenas": {
                "inicio": {
                    "id": "inicio",
                    "texto": "Sua aventura começa aqui. Edite o arquivo historia.json para personalizar sua história.",
                    "opcoes": {},
                    "final": False
                }
            },
            "config": {
                "titulo": "Aventura Personalizada",
                "personagem_principal": "Herói",
                "version": "1.0"
            }
        }
        salvar_historia(historia_base)
        print("Arquivo historia.json criado com estrutura básica.")
    
    app.run(host="0.0.0.0", port=5000, debug=True)