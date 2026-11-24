const INTERVALO_MS = 60 * 1000; // relê o arquivo local a cada 1 min (é barato)
const container = document.getElementById("cardsContainer");
const metaInfo = document.getElementById("metaInfo");

const ESCAPES = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
const escapar = (t) => String(t ?? "").replace(/[&<>"']/g, (c) => ESCAPES[c]);

function agrupar(ocorrencias) {
  const grupos = {};
  for (const item of ocorrencias) {
    const chave = `${item.concessionaria}||${item.rodovia}`;
    grupos[chave] ??= {
      concessionaria: item.concessionaria,
      rodovia: item.rodovia,
      prioridade: item.prioridade,
      itens: [],
    };
    grupos[chave].itens.push(item);
    grupos[chave].prioridade = Math.min(grupos[chave].prioridade, item.prioridade);
  }
  return Object.values(grupos).sort(
    (a, b) => a.prioridade - b.prioridade || b.itens.length - a.itens.length
  );
}

const CATEGORIA_POR_PRIORIDADE = { 1: "acidente", 2: "obras" };

function htmlOcorrencia(oc) {
  const latlong = oc.latitude != null && oc.longitude != null
    ? `${oc.latitude}, ${oc.longitude}` : "-";
  return `
    <div class="ocorrencia-item alerta-${oc.categoria}">
      <div class="ocorrencia-topo">
        <span class="badge"><b>Sentido:</b> ${escapar(oc.sentido || "-")}</span>
        <span class="badge"><b>Tipo:</b> ${escapar(oc.tipo || "-")}</span>
      </div>
      <p class="desc">${escapar(oc.descricao) || "Sem descrição detalhada."}</p>
      <div class="latlong">Lat/Long: ${latlong}</div>
    </div>`;
}

function htmlGrupo(grupo) {
  const categoria = CATEGORIA_POR_PRIORIDADE[grupo.prioridade] ?? "normal";
  const classeConc = grupo.concessionaria.toLowerCase() === "arteris"
    ? "conc-arteris" : "conc-motiva";
  return `
    <div class="grupo-card alerta-${categoria}">
      <div class="grupo-header">
        <div class="rodovia-nome" title="${escapar(grupo.rodovia)}">
          ${escapar(grupo.rodovia)} (${grupo.itens.length})
        </div>
        <span class="conc-tag ${classeConc}">${escapar(grupo.concessionaria)}</span>
      </div>
      <div class="lista-ocorrencias">${grupo.itens.map(htmlOcorrencia).join("")}</div>
    </div>`;
}

function desenhar({ atualizado_em, ocorrencias }) {
  const grupos = agrupar(ocorrencias);
  metaInfo.textContent =
    `Atualizado em: ${atualizado_em} • ${ocorrencias.length} ocorrência(s) em ${grupos.length} rodovia(s)`;
  container.innerHTML = grupos.length
    ? grupos.map(htmlGrupo).join("")
    : `<div class="vazio">Sem ocorrências ativas no momento.</div>`;
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
