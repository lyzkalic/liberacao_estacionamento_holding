document.addEventListener("DOMContentLoaded", () => {
    // Mapeamento dos elementos do formulário
    const campoCpf = document.getElementById("filtroCpf");
    const campoUsuario = document.getElementById("filtroUsuario");
    const campoTipoAcao = document.getElementById("filtroTipoAcao");
    const campoStatus = document.getElementById("filtroStatus");
    const campoDataInicial = document.getElementById("filtroDataInicial");
    const campoDataFinal = document.getElementById("filtroDataFinal");

    function definirDataAtual() {
    const hoje = new Date();

    // Formata para yyyy-MM-dd (formato aceito pelo input type="date")
    const dataHoje = hoje.toISOString().split("T")[0];

    if (campoDataInicial) {
        campoDataInicial.value = dataHoje;
    }

    if (campoDataFinal) {
        campoDataFinal.value = dataHoje;
    }
}
    
    // Mapeamento de estrutura
    const corpoTabela = document.getElementById("corpoTabela");
    const tabelaContainer = document.getElementById("tabelaContainer");
    const mensagem = document.getElementById("mensagem");
    const btnPesquisar = document.getElementById("btnPesquisar");
    const btnExportar = document.getElementById("btnExportar");

    // Mapeamento da Gaveta Lateral (Sidebar)
    const sidebarDetalhes = document.getElementById("sidebarDetalhes");
    const btnFecharSidebar = document.getElementById("btnFecharSidebar");

    // Coleta os valores digitados nos filtros
    function obterFiltros() {
        return {
            cpf: campoCpf ? campoCpf.value || null : null,
            usuario: campoUsuario ? campoUsuario.value || null : null,
            tipo_acao: campoTipoAcao ? campoTipoAcao.value || null : null,
            status: campoStatus ? campoStatus.value || null : null,
            data_inicial: campoDataInicial ? campoDataInicial.value || null : null,
            data_final: campoDataFinal ? campoDataFinal.value || null : null
        };
    }

    // Exibe mensagem de erro se a busca falhar
    function exibirErro(texto) {
        if (!mensagem) return;
        mensagem.innerHTML = `
            <div class="feedback-erro">
                <p>🔴 <strong>Atenção:</strong> ${texto}</p>
            </div>
        `;
    }

    // Função que abre a gaveta lateral com as informações detalhadas
    function abrirDetalhes(registro) {
        if (!sidebarDetalhes) return;

        document.getElementById("detalheData").innerText = formatarDataHora(registro.data_liberacao);
        document.getElementById("detalheUsuario").innerText = registro.usuario || "-";
        document.getElementById("detalheResultado").innerText = registro.status || registro.tipo_acao || "-";
        document.getElementById("detalheMensagem").innerText = registro.mensagem || "Nenhuma mensagem detalhada gravada.";

        sidebarDetalhes.classList.add("aberta");
    }

    // Fecha a gaveta lateral
    if (btnFecharSidebar) {
        btnFecharSidebar.addEventListener("click", () => {
            sidebarDetalhes.classList.remove("aberta");
        });
    }

    function formatarDataHora(data) {
    if (!data) return "-";

    return new Date(data).toLocaleString("pt-BR", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit"
        });
    }

    // Desenha as linhas na tabela
    function renderizarTabela(registros) {
        if (!corpoTabela) return;

        corpoTabela.innerHTML = "";

        if (!registros || registros.length === 0) {
            corpoTabela.innerHTML = `
                <tr>
                    <td colspan="9" style="text-align: center; padding: 20px;">
                        Nenhum registro encontrado para os filtros selecionados.
                    </td>
                </tr>`;
            if (tabelaContainer) tabelaContainer.style.display = "block";
            return;
        }

        registros.forEach((registro) => {
            const linha = document.createElement("tr");
            const dataLiberacaoDisplay = formatarDataHora(registro.data_liberacao);
              new Date(registro.data_liberacao).toLocaleString("pt-BR", {
                 day: "2-digit",
                 month: "2-digit",
                 year: "numeric",
                 hour: "2-digit",
                 minute: "2-digit",
                 second: "2-digit"
                })

            const cpfDisplay = registro.cpf_cliente || "-";
            const ticketDisplay = registro.numero_ticket || "-";
            const transacaoDisplay = registro.id_transacao || "-";
            const garagemDisplay = registro.id_garagem || "-";
            const perfilDisplay = registro.perfil || "-";
            const statusDisplay = registro.status || registro.tipo_acao || "SUCESSO";


            linha.innerHTML = `
                <td>${dataLiberacaoDisplay}</td>
                <td>${registro.usuario || "-"}</td>
                <td>${perfilDisplay}</td>
                <td>${cpfDisplay}</td>
                <td>${ticketDisplay}</td>
                <td>${transacaoDisplay}</td>
                <td>${garagemDisplay}</td>
                <td>${statusDisplay}</td>
                <td>
                    <button type="button" class="btn-detalhes">Ver detalhes</button>
                </td>
            `;

            // Adiciona evento de clique no botão de detalhes da linha
            const btnDetalhes = linha.querySelector(".btn-detalhes");
            if (btnDetalhes) {
                btnDetalhes.addEventListener("click", () => abrirDetalhes(registro));
            }

            corpoTabela.appendChild(linha);
        });

        // Revela a tabela na tela
        if (tabelaContainer) {
            tabelaContainer.style.display = "block";
        }
    }

    // Função principal de Pesquisa (Consulta ao Servidor)
    async function pesquisar() {
        if (mensagem) mensagem.innerHTML = "";

        try {
            const resposta = await fetch("/auditoria/pesquisar", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(obterFiltros())
            });

            const dados = await resposta.json();

            if (dados.sucesso) {
                renderizarTabela(dados.dados);
            } else {
                exibirErro(dados.mensagem || "Não foi possível carregar o histórico.");
            }
        } catch (erro) {
            console.error("Erro na consulta:", erro);
            exibirErro("Erro de comunicação com o servidor.");
        }
    }

    // Função de Exportação
    function exportar() {
        const filtros = obterFiltros();
        const parametros = new URLSearchParams();

        Object.keys(filtros).forEach((chave) => {
            if (filtros[chave]) {
                parametros.append(chave, filtros[chave]);
            }
        });

        window.location.href = "/auditoria/exportar?" + parametros.toString();
    }

    // Atribuição dos botões
    if (btnPesquisar) btnPesquisar.addEventListener("click", pesquisar);
    if (btnExportar) btnExportar.addEventListener("click", exportar);

    definirDataAtual();
    pesquisar();
});
