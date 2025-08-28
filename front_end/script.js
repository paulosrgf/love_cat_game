const historiaDiv = document.getElementById('historia');
const opcoesDiv = document.getElementById('opcoes');
let cenaAtualId = 'inicio';

// Função para avançar no jogo
async function avancarJogo(escolha) {
    try {
        mostrarLoading();
        
        console.log(`Enviando: escolha=${escolha}, cena_atual=${cenaAtualId}`);
        
        const response = await fetch('/avancar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                escolha: escolha,
                cena_atual: cenaAtualId
            }),
        });
        
        console.log(`Resposta recebida: ${response.status}`);
        
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Erro do servidor (${response.status}): ${errorText}`);
        }
        
        const dados = await response.json();
        console.log('Dados recebidos:', dados);
        
        if (dados.erro) {
            throw new Error(dados.erro);
        }
        
        exibirCena(dados);
        cenaAtualId = dados.id;
        
    } catch (error) {
        console.error('Erro detalhado:', error);
        mostrarErro(`Erro: ${error.message}`);
    }
}

// Função para exibir a cena
function exibirCena(cena) {
    historiaDiv.innerHTML = `<p>${cena.texto}</p>`;
    opcoesDiv.innerHTML = ''; // Limpa as opções anteriores

    // Verifica se é um final
    if (cena.final) {
        const botaoReiniciar = document.createElement('button');
        botaoReiniciar.textContent = '🎮 Jogar Novamente';
        botaoReiniciar.onclick = reiniciarJogo;
        botaoReiniciar.style.backgroundColor = '#4CAF50';
        opcoesDiv.appendChild(botaoReiniciar);
        return;
    }

    // Cria os botões para cada opção
    for (const [key, value] of Object.entries(cena.opcoes)) {
        const botao = document.createElement('button');
        // Formata o texto da opção (remove underscores e capitaliza)
        botao.textContent = key
            .split('_')
            .map(palavra => palavra.charAt(0).toUpperCase() + palavra.slice(1))
            .join(' ');
        botao.onclick = () => avancarJogo(key); // Envia a chave, não o valor
        opcoesDiv.appendChild(botao);
    }
}

// Função para mostrar loading
function mostrarLoading() {
    historiaDiv.innerHTML = '<p class="loading">Carregando...</p>';
    opcoesDiv.innerHTML = '';
}

// Função para mostrar erro
function mostrarErro(mensagem) {
    historiaDiv.innerHTML = `<p class="error">${mensagem}</p>`;
    
    const botaoReiniciar = document.createElement('button');
    botaoReiniciar.textContent = '🔄 Tentar Novamente';
    botaoReiniciar.onclick = reiniciarJogo;
    opcoesDiv.innerHTML = '';
    opcoesDiv.appendChild(botaoReiniciar);
}

// Reiniciar o jogo
function reiniciarJogo() {
    cenaAtualId = 'inicio';
    iniciar();
}

// Inicia o jogo
async function iniciar() {
    try {
        mostrarLoading();
        console.log('Iniciando jogo...');
        
        const response = await fetch('/iniciar');
        console.log(`Resposta inicial: ${response.status}`);
        
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Erro do servidor (${response.status}): ${errorText}`);
        }
        
        const dados = await response.json();
        console.log('Dados iniciais:', dados);
        
        if (dados.erro) {
            throw new Error(dados.erro);
        }
        
        exibirCena(dados);
        cenaAtualId = dados.id;
        
    } catch (error) {
        console.error('Erro ao iniciar:', error);
        mostrarErro(`Erro ao iniciar: ${error.message}`);
    }
}

// Inicia o jogo quando a página carrega
document.addEventListener('DOMContentLoaded', iniciar);