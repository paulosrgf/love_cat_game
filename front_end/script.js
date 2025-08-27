const historiaDiv = document.getElementById('historia');
const opcoesDiv = document.getElementById('opcoes');

// Função para avançar no jogo abubleble
async function avancarJogo(escolha) {
    const response = await fetch('http://127.0.0.1:5000/avancar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ escolha: escolha }),
    });
    const dados = await response.json();
    exibirCena(dados);
}

// Função para exibir a cena blablabla
function exibirCena(cena) {
    historiaDiv.textContent = cena.texto;
    opcoesDiv.innerHTML = ''; // Limpa as opções anteriores

    // Cria os botões para cada opção
    for (const [key, value] of Object.entries(cena.opcoes)) {
        const botao = document.createElement('button');
        botao.textContent = key.replace(/_/g, ' '); // Substitui '_' por espaço
        botao.onclick = () => avancarJogo(value);
        opcoesDiv.appendChild(botao);
    }
}

// Inicia o jogo aaaaaai
async function iniciar() {
    const response = await fetch('http://127.0.0.1:5000/iniciar');
    const dados = await response.json();
    exibirCena(dados);
}

iniciar();