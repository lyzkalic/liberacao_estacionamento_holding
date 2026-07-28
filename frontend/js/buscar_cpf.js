const formulario = document.getElementById("formCpf");
const campoCpf = document.getElementById("cpf");
const mensagem = document.getElementById("mensagem");

function exibirSucesso(cliente, beneficio) {

    mensagem.innerHTML = `
        <div class="feedback feedback-sucesso">
            <p class="feedback-titulo">Cupom encontrado!</p>
            <p><strong>Cliente:</strong> <span id="feedbackCliente"></span></p>
            <p><strong>Benefício:</strong> <span id="feedbackBeneficio"></span></p>
            <a href="/liberar" class="btn btn-secondary">Continuar</a>
        </div>
    `;

    document.getElementById("feedbackCliente").textContent = cliente;
    document.getElementById("feedbackBeneficio").textContent = beneficio;

}

function exibirErro(texto) {

    mensagem.innerHTML = `
        <div class="feedback feedback-erro">
            <p class="feedback-titulo" id="feedbackErro"></p>
        </div>
    `;

    document.getElementById("feedbackErro").textContent = texto;

}

if (!formulario || !campoCpf) {
    console.error("Elementos da página não encontrados.");
} else {

    formulario.addEventListener("submit", async (event) => {

        event.preventDefault();

        const resposta = await fetch("/buscar-cupom", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                cpf: campoCpf.value
            })
        });

        const dados = await resposta.json();

        if (dados.sucesso) {

    const cupom = dados.dados;

    sessionStorage.setItem("cliente_nome", cupom.cliente_nome);
    sessionStorage.setItem("beneficio", cupom.beneficio);
    sessionStorage.setItem("cpf", campoCpf.value);

    exibirSucesso(
        cupom.cliente_nome,
        cupom.beneficio
    );

} else {

    exibirErro(dados.mensagem);

}

    });

}
