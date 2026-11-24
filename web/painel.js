const INTERVALO_MS = 60 * 1000; // relê o dados.json a cada 1 minuto

const metaInfo = document.getElementById("metaInfo");
const listaAcidentes = document.getElementById("listaAcidentes");
const listaAtencao = document.getElementById("listaAtencao");
const contAcidentes = document.getElementById("contAcidentes");
const contAtencao = document.getElementById("contAtencao");

const ESCAPES = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
const escapar = (t) => String(t ?? "").replace(/[&<>"']/g, (c) => ESCAPES[c]);

/* Agrupa por concessionária + rodovia; os grupos mais urgentes e mais cheios vêm primeiro */
function agrupar(ocorrencias) {
  const grupos = {};
  for (const item of ocorrencias) {
    const chave = `${item.concessionaria}||${item.rodovia}`;
    grupos[chave] ??= {
      concessionaria: item.concessionaria,
      rodovia: item.rodovia,
      prioridade: item.prioridade,
      categoria: item.categoria,
      itens: [],
    };
    grupos[chave].itens.push(item);
    if (item.prioridade < grupos[chave].prioridade) {
      grupos[chave].prioridade = item.prioridade;
      grupos[chave].categoria = item.categoria;
    }
  }
  return Object.values(grupos).sort(
    (a, b) => a.prioridade - b.prioridade || b.itens.length - a.itens.length
  );
}

function htmlOcorrencia(oc) {
  const latlong = oc.latitude != null && oc.longitude != null
    ? `${oc.latitude}, ${oc.longitude}` : "-";
  return `
    <div class="ocorrencia ${escapar(oc.categoria)}">
      <p class="tipo">${escapar(oc.tipo || "-")}</p>
      <span class="sentido">Sentido: ${escapar(oc.sentido || "-")}</span>
      <p class="desc">${escapar(oc.descricao) || "Sem descrição detalhada."}</p>
      <div class="latlong">Lat/Long: ${latlong}</div>
    </div>`;
}

function htmlCartao(grupo) {
  const classeEtiqueta = grupo.concessionaria.toLowerCase() === "arteris"
    ? "etiqueta-arteris" : "etiqueta-motiva";
  return `
    <article class="cartao ${escapar(grupo.categoria)}">
      <div class="cartao-topo">
        <div class="rodovia-nome" title="${escapar(grupo.rodovia)}">
          ${escapar(grupo.rodovia)} (${grupo.itens.length})
        </div>
        <span class="etiqueta ${classeEtiqueta}">${escapar(grupo.concessionaria)}</span>
      </div>
      <div class="ocorrencias">${grupo.itens.map(htmlOcorrencia).join("")}</div>
    </article>`;
}

function preencher(caixa, contador, ocorrencias, mensagemVazia) {
  const grupos = agrupar(ocorrencias);
  contador.textContent = `(${ocorrencias.length})`;
  caixa.innerHTML = grupos.length
    ? grupos.map(htmlCartao).join("")
    : `<div class="vazio">${mensagemVazia}</div>`;
}

function desenhar({ atualizado_em, ocorrencias }) {
  const acidentes = ocorrencias.filter((o) => o.categoria === "acidente");
  const atencao = ocorrencias.filter((o) => o.categoria !== "acidente");

  metaInfo.textContent =
    `Atualizado em: ${atualizado_em} • ${ocorrencias.length} ocorrência(s)`;

  preencher(listaAcidentes, contAcidentes, acidentes, "Nenhum acidente registrado no momento.");
  preencher(listaAtencao, contAtencao, atencao, "Nenhum ponto de atenção no momento.");
}

async function atualizar() {
  try {
    const resp = await fetch("dados.json", { cache: "no-store" });
    if (!resp.ok) throw new Error(resp.status);
    desenhar(await resp.json());
  } catch (erro) {
    metaInfo.textContent = "Aguardando a primeira coleta...";
  }
}

atualizar();
setInterval(atualizar, INTERVALO_MS);
