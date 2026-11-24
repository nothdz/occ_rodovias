# Monitor de Ocorrências nas Rodovias

Painel que reúne, em uma única página, as ocorrências de trânsito (acidentes, obras, interdições etc.) divulgadas pelas concessionárias **Motiva** e **Arteris**. Os acidentes aparecem em destaque vermelho e as obras em laranja.

**Painel no ar:** https://nothdz.github.io/occ_rodovias/

---

## Como funciona

```
┌────────────────────┐     ┌──────────────┐     ┌──────────────────┐
│  Motiva e Arteris  │ ──► │ Coleta em    │ ──► │ web/dados.json   │
│                    │     │ Python       │     │                  │
└────────────────────┘     └──────────────┘     └────────┬─────────┘
                                                         │ lido pela página
                                                         ▼
                                              ┌──────────────────────┐
                                              │ web/index.html       │
                                              │ (painel no navegador)│
                                              └──────────────────────┘
```

1. O Python consulta todos os trechos **ao mesmo tempo** (várias threads), junta os resultados, remove repetidos e classifica por urgência.
2. O resultado é gravado em `web/dados.json`.
3. A página (`index.html` + `estilo.css` + `painel.js`) lê o `dados.json` sozinha a cada 1 minuto e redesenha os cartões, sem recarregar.

A coleta (Python) e a interface (HTML, CSS e JS) são totalmente separadas: o único contato entre elas é o arquivo `dados.json`.

---

## Estrutura do projeto

```
.
├── .github/workflows/
│   └── atualizar.yml        # agendamento e publicação automática
├── web/
│   ├── index.html           # estrutura da página
│   ├── estilo.css           # aparência
│   └── painel.js            # lê o dados.json e monta os cartões
├── configuracao.py          # trechos, cabeçalhos, intervalo, porta, tempo limite
├── modelos.py               # estrutura de dados da ocorrência
├── classificacao.py         # regra de prioridade (acidente > obras > normal)
├── motiva.py                # coleta de um trecho da Motiva
├── arteris.py               # coleta de um trecho da Arteris
├── coleta.py                # coleta todos os trechos em paralelo
├── saida.py                 # grava o dados.json
├── servidor.py              # servidor local simples (só para uso local)
├── principal.py             # modo local contínuo: coleta + servidor
├── coletar_uma_vez.py       # coleta uma vez e termina (usado na publicação)
└── requirements.txt         # dependências
```

---

## Requisitos

- **Python 3.10 ou superior**
- Biblioteca **requests** (já listada em `requirements.txt`)
- Biblioteca **truststore**, necessária apenas para rodar o `principal.py` no Windows (usa os certificados do sistema, útil em redes com proxy corporativo)
- Conexão com a internet

---

## Executar no seu computador

### 1. Preparar o ambiente

```bash
# criar um ambiente isolado (recomendado)
python -m venv .venv

# ativar no Windows (PowerShell)
.venv\Scripts\Activate.ps1
# ativar no Linux/Mac
source .venv/bin/activate

# instalar as dependências
pip install -r requirements.txt
pip install truststore
```

### 2. Escolher o modo

**Modo contínuo** (coleta de tempos em tempos e já abre um servidor local):

```bash
python principal.py
```

Depois abra http://localhost:8050/ no navegador. O programa coleta a cada 30 minutos (`INTERVALO_SEGUNDOS` em `configuracao.py`). Para parar, use `Ctrl + C`.

**Coleta única** (gera o `web/dados.json` e termina):

```bash
python coletar_uma_vez.py
```

Para ver a página nesse modo, suba um servidor na pasta `web`:

```bash
python -m http.server 8050 --directory web
```

> A página precisa ser aberta por um servidor (`http://...`). Abrir o `index.html` com duplo clique (`file://...`) não funciona, porque o navegador bloqueia a leitura do `dados.json`.

---

## Publicar na web (de graça)

A publicação usa o **GitHub Actions** (agendador) e o **GitHub Pages** (hospedagem). Em repositório **público**, o uso é gratuito. Nada precisa ficar rodando no seu computador.

### Primeira publicação

1. Crie um repositório **público** no GitHub e envie todo o projeto, incluindo as pastas `web/` e `.github/workflows/`.
2. No repositório, abra **Settings → Pages**. Em **Build and deployment → Source**, escolha **GitHub Actions**. Não clique em "Configure" nos modelos sugeridos e deixe o campo "Custom domain" vazio.
3. Abra a aba **Actions**, escolha o fluxo **Atualizar painel** e clique em **Run workflow**.
4. Aguarde os dois blocos (**coletar** e **publicar**) ficarem verdes (cerca de 1 minuto).
5. O painel estará em `https://SEU-USUARIO.github.io/NOME-DO-REPOSITORIO/`.

### Atualização automática

O arquivo `.github/workflows/atualizar.yml` tem um agendamento (`cron`) que repete o processo sozinho. O intervalo mínimo aceito pelo GitHub é de **5 minutos**:

```yaml
on:
  schedule:
    - cron: "*/5 * * * *"
```

Para mudar o intervalo, altere esse valor (por exemplo, `"*/30 * * * *"` para 30 minutos) e salve.

Para conferir se o agendamento funciona, espere alguns minutos e veja na aba **Actions** novas execuções com o evento **schedule**, ou observe o horário "Atualizado em" no topo do painel.

### Cuidados com a publicação

- **Desligamento por inatividade:** em repositório público, o GitHub desativa os agendamentos se o repositório ficar **60 dias sem atividade**. Se o painel parar de atualizar, vá em **Actions**, reative o fluxo e rode uma vez. Um commit qualquer de vez em quando também evita isso.
- **Atrasos:** o GitHub pode atrasar ou pular execuções agendadas em horários de pico, então o intervalo real pode ser maior que o configurado.
- **Código público:** qualquer pessoa pode ver o repositório. Não coloque senhas, chaves ou dados sigilosos nele.

---

## Configuração

Tudo fica em `configuracao.py`:

| Item | O que faz |
|---|---|
| `TRECHOS_MOTIVA` | Trechos da Motiva (nome do trecho → endereço da API). O nome segue o padrão `Rodovia - Sentido X`. |
| `TRECHOS_ARTERIS` | Trechos da Arteris. |
| `CABECALHOS_MOTIVA` / `CABECALHOS_ARTERIS` | Cabeçalhos enviados nas requisições. |
| `MAX_THREADS` | Quantas consultas rodam ao mesmo tempo (padrão: 8). |
| `TIMEOUT` | Tempo máximo de espera por resposta, em segundos. |
| `INTERVALO_SEGUNDOS` | Intervalo da coleta no modo local contínuo. |
| `PORTA_PAINEL` | Porta do servidor local. |

### Adicionar um trecho

Inclua uma nova linha em `TRECHOS_MOTIVA` ou `TRECHOS_ARTERIS`. Não é preciso mexer em mais nada.

### Adicionar outra concessionária

1. Crie um arquivo novo (por exemplo, `outraconcessionaria.py`) com uma função `coletar_trecho(nome, url)` que devolve uma lista de `Ocorrencia` (veja `arteris.py` como modelo).
2. Registre os trechos dela em `configuracao.py`.
3. Inclua as tarefas dela em `coleta.py`.

### Mudar a regra de prioridade

Edite `classificacao.py`. Hoje, texto com "acidente" é prioridade 1 (vermelho), com "obras" é prioridade 2 (laranja) e o restante é prioridade 3.

---

## Problemas comuns

| Sintoma | Causa provável e solução |
|---|---|
| `No such file or directory ... web\dados.json.tmp` | A pasta `web/` não existe. Crie-a (a versão atual do `saida.py` já cria sozinha). |
| Página em branco ou "Aguardando a primeira coleta..." | Ainda não existe `dados.json`. Rode a coleta uma vez. |
| Página não carrega ao abrir o `index.html` direto | Abra por um servidor, como explicado em "Executar no seu computador". |
| Erro `No artifacts named "github-pages"` na publicação | Use a estrutura de dois blocos do `atualizar.yml` e `upload-pages-artifact@v4`. |
| Aviso vermelho sobre "custom domain" em Settings → Pages | Deixe o campo de domínio próprio vazio. Se persistir, apague um arquivo `CNAME` do repositório. |
| Painel desatualizado | Veja a aba **Actions**: o agendamento pode ter sido desativado por inatividade ou as APIs podem ter mudado. |
| `[trecho] falhou: ...` no terminal | A API daquele trecho não respondeu ou mudou. Os outros trechos continuam normalmente. |

---

## Pontos de atenção

- Os trechos **Anhanguera (SP-330)** e **Bandeirantes (SP-348)** estão com o mesmo endereço (`origin`/`destination`) nos sentidos Norte e Sul. Isso faz as mesmas ocorrências aparecerem duas vezes, com sentidos diferentes. Convém inverter `origin` e `destination` em um dos lados, como já está na Dutra e na Rodovia do Café.
- Os dados vêm de endereços públicos usados pelos sites das concessionárias. Se elas mudarem o formato ou passarem a bloquear as consultas, o painel pode parar de funcionar.

---

## Aviso

Projeto independente, sem vínculo com a Motiva, a Arteris ou o GitHub. As informações exibidas são de responsabilidade das concessionárias e podem ter atraso ou estar incompletas. Não use o painel como única fonte para decisões de segurança.
