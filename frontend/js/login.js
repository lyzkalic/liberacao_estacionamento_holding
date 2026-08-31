const formulario = document.getElementById("formLogin");
const campoUsuario = document.getElementById("usuario");
const campoSenha = document.getElementById("senha");
const mensagem = document.getElementById("mensagem");

function exibirErro(texto) {
    if (!mensagem) return;
    
    mensagem.innerHTML = `
        <div class="feedback feedback-erro">
            <p class="feedback-titulo" id="feedbackErro"></p>
        </div>
    `;

    const elementoErro = document.getElementById("feedbackErro");
    if (elementoErro) {
        elementoErro.textContent = texto;
    }
}

if (!formulario || !campoUsuario || !campoSenha) {
    console.error("Elementos da página não encontrados.");
} else {
    formulario.addEventListener("submit", async (event) => {
        event.preventDefault();

        try {
            const resposta = await fetch("/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    usuario: campoUsuario.value,
                    senha: campoSenha.value
                })
            });

            const dados = await resposta.json();

            if (dados.sucesso) {
                // Redireciona para a URL enviada pelo backend (/buscar) ou fallback para /buscar
                window.location.href = dados.redirect_url || "/buscar";
            } else {
                exibirErro(dados.mensagem || dados.detail || "Erro ao efetuar login.");
            }
        } catch (erro) {
            console.error("Erro na requisição:", erro);
            exibirErro("Serviço indisponível no momento.");
        }
    });
}