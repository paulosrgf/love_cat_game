# 🐱 Aventura do Bartolomeu - Gato do Amor

Uma aventura interativa onde você guia Bartolomeu, um gato charmoso, em sua jornada para conquistar Julieta.

## 🚀 Como executar o projeto

### Pré-requisitos
- Python 3.8 ou superior
- Git

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/nome-do-repositorio.git
cd nome-do-repositorio

2. Crie e ative um ambiente virtual
bash

# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate

3. Instale as dependências
bash

pip install -r requirements.txt

4. Execute a aplicação
bash

cd back_end
python app.py

5. Acesse o jogo

Abra seu navegador e vá para: http://localhost:5000
🎮 Como jogar

    Leia a história que aparece na tela

    Escolha uma das opções clicando nos botões

    Tome decisões que afetam o destino do Bartolomeu

    Descobre todos os finais possíveis!

📁 Estrutura do projeto
text

aventura-bartolomeu/
├── back_end/           # Código backend (Flask)
│   ├── app.py         # Aplicação principal
│   ├── historia.json  # História em JSON
│   └── __init__.py
├── front_end/         # Interface web
│   ├── index.html     # Página principal
│   ├── style.css      # Estilos
│   └── script.js      # Lógica do jogo
├── requirements.txt   # Dependências Python
└── README.md         # Este arquivo

🛠️ Tecnologias utilizadas

    Backend: Python + Flask

    Frontend: HTML5 + CSS3 + JavaScript

    Arquitetura: API RESTful

✨ Recursos

    ✅ História interativa com múltiplos finais

    ✅ Interface responsiva e temática

    ✅ Sistema de escolhas que alteram o enredo

    ✅ Reinício automático ao finalizar

🎯 Possíveis finais

    💔 Final triste (observar de longe)

    😻 Final romântico (elogio)

    🐾 Final aventureiro (ajuda)

🔧 Desenvolvimento
Modificando a história

Edite o arquivo back_end/historia.json para adicionar novas cenas e opções.
Adicionando uma nova cena
json

{
  "id": "nova_cena",
  "texto": "Texto da nova cena...",
  "opcoes": {
    "opcao1": "proxima_cena1",
    "opcao2": "proxima_cena2"
  },
  "final": false
}

Executando em modo desenvolvimento
bash

cd back_end
python app.py

🤝 Contribuindo

    Faça um fork do projeto

    Crie uma branch para sua feature (git checkout -b feature/AmazingFeature)

    Commit suas mudanças (git commit -m 'Add some AmazingFeature')

    Push para a branch (git push origin feature/AmazingFeature)

    Abra um Pull Request

📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
👥 Autores

    Helena Costa - @lenacs06
    Paulo sergio - @paulosrgf

⭐️ Se você gostou do projeto, deixe uma estrela no GitHub!

