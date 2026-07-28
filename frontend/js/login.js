const formulario = document.getElementById("formLogin");
const campoUsuario = document.getElementById("usuario");
const campoSenha = document.getElementById("senha");
const mensagem = document.getElementById("mensagem");

function exibirErro(texto) {

    mensagem.innerHTML = `
        <div class="feedback feedback-erro">
            <p class="feedback-titulo" id="feedbackErro"></p>
        </div>
    `;

    document.getElementById("feedbackErro").textContent = texto;

}

if (!formulario || !campoUsuario || !campoSenha) {
    console.error("Elementos da página não encontrados.");
} else {

    formulario.addEventListener("submit", async (event) => {

        event.preventDefault();

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

            window.location.href = "/";

        } else {

            exibirErro(dados.mensagem);

        }

    });

}
