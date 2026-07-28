console.log("liberar_ticket.js carregado");
console.log("========== LIBERAR TICKET ==========");
console.log("cliente_nome:", sessionStorage.getItem("cliente_nome"));
console.log("beneficio:", sessionStorage.getItem("beneficio"));
console.log("cpf:", sessionStorage.getItem("cpf"));
console.log("====================================");

const formulario = document.getElementById("formTicket");
const campoTicket = document.getElementById("ticket");
const mensagem = document.getElementById("mensagem");

document.getElementById("nomeCliente").textContent = sessionStorage.getItem("cliente_nome") || "";
document.getElementById("beneficio").textContent = sessionStorage.getItem("beneficio") || "";

function exibirSucesso(texto) {

    mensagem.innerHTML = `
        <div class="feedback feedback-sucesso">
            <span class="feedback-icon">🟢</span>
            <p class="feedback-titulo" id="feedbackSucesso"></p>
        </div>
    `;

    document.getElementById("feedbackSucesso").textContent = texto;

}

function exibirErro(texto) {

    mensagem.innerHTML = `
        <div class="feedback feedback-erro">
            <span class="feedback-icon">🔴</span>
            <p class="feedback-titulo" id="feedbackErro"></p>
        </div>
    `;

    document.getElementById("feedbackErro").textContent = texto;

}

formulario.addEventListener("submit", async function(event) {

    event.preventDefault();

    console.log("Submit executado");

    const cpf = sessionStorage.getItem("cpf");

    console.log("CPF antes do fetch:", cpf);

    const payload = {
        cpf: cpf,
        numero_ticket: campoTicket.value
    };

    console.log("Payload:", payload);

    try {

        const response = await fetch("/liberar-ticket", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        console.log("Status HTTP:", response.status);

        const dados = await response.json();

        console.log("Resposta:", dados);

        if (dados.sucesso) {
            exibirSucesso(dados.mensagem);
        } else {
            exibirErro(dados.mensagem);
        }

    } catch (error) {

        exibirErro("Erro ao comunicar com o servidor.");
        console.error(error);

    }

});

console.log("Listener registrado");
