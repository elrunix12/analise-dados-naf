# 📊 Dashboard Analítico NAF (Núcleo de Apoio Contábil e Fiscal)

Dashboard interativo desenvolvido em Single Page Application (SPA) para analisar e visualizar os dados de atendimentos registrados nas planilhas do NAF. 

A ferramenta foi construída com uma **Arquitetura Híbrida**, permitindo o processamento local via CSV (completamente offline) ou a conexão direta em tempo real com o Google Sheets via Google Apps Script.

## 🚀 Principais Funcionalidades

* **Arquitetura Híbrida (Feature Toggle):** Alternância simples entre leitura de CSV (PapaParse) e integração com banco de dados em nuvem (Google Apps Script).
* **Visão em Abas Estruturadas:** Dados segmentados nas visões *Geral*, *Operacional (Serviços)* e *Perfil do Contribuinte* para facilitar a análise.
* **Higienização de Dados:** Padronização automática de strings (conversão para maiúsculas, remoção de acentos e espaços extras) para evitar duplicidade na contagem das categorias.
* **Desmembramento de Atendimentos Múltiplos:** Identifica quando o usuário seleciona múltiplos serviços no formulário e contabiliza de forma correta, sem distorcer o número total de pessoas físicas atendidas.
* **Filtros Dinâmicos Multi-nível:** Análise granular através de filtros combinados globais (`Ano`, `Mês`, `Município`) e locais (`Público`, `Conclusão`, `Serviço`, `Gênero`).
* **Modo de Rótulos de Dados (Exportação):** Botão integrado (ícone de olho) para ligar/desligar os números exatos nos gráficos, preparando o painel para salvamento nativo de imagens em PNG.

---

## ⚙️ Modos de Operação (Como Executar)

O sistema possui uma "Chave Mestra" logo no início do código JavaScript (`index.html`), na variável `USAR_GOOGLE_SHEETS`.

### Modo 1: Offline com CSV (Padrão)
**Configuração:** `const USAR_GOOGLE_SHEETS = false;`

Neste modo, não é necessário instalar nenhum servidor. O processamento respeita integralmente a LGPD, mantendo os dados apenas no navegador do usuário.
1. Abra o Google Sheets vinculado ao seu Google Forms e baixe a planilha: `Arquivo > Fazer download > Valores separados por vírgulas (.csv)`.
2. Dê um duplo clique no arquivo `index.html` no seu computador para abrir o painel.
3. Clique em **Carregar** e selecione o arquivo CSV.

### Modo 2: Integrado na Nuvem (Google Sheets)
**Configuração:** `const USAR_GOOGLE_SHEETS = true;`

Neste modo, o painel roda diretamente dentro da sua planilha do Google, lendo os dados em tempo real da aba que estiver ativa.
1. Abra sua planilha do Google Sheets.
2. Vá no menu superior em **Extensões > Apps Script**.
3. Crie/renomeie o arquivo HTML para `index.html` e cole todo o código do Dashboard lá (lembre-se de mudar a variável para `true`).
4. Crie/renomeie o arquivo de script para `Código.gs` e cole o código backend abaixo.
5. Salve tudo. Volte para a planilha, atualize a página (F5) e use o novo menu **📊 Analytics NAF** que aparecerá no topo.

<details>
<summary><b>Clique aqui para copiar o arquivo Código.gs (Backend)</b></summary>

```javascript
// Função que renderiza a página HTML (Para Web App)
function doGet() {
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('Dashboard NAF')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

// Cria o menu customizado na Planilha
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('📊 Analytics NAF')
    .addItem('Abrir Dashboard', 'abrirDashboard')
    .addToUi();
}

function abrirDashboard() {
  const html = HtmlService.createHtmlOutputFromFile('index')
    .setTitle('Dashboard Analítico NAF')
    .setWidth(1200)
    .setHeight(800);
  SpreadsheetApp.getUi().showModalDialog(html, 'Dashboard Analítico NAF');
}

// O "Motor" que extrai os dados para o JavaScript do painel
function obterDadosPlanilha() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const data = sheet.getDataRange().getDisplayValues(); // Pega tudo como texto
  
  if (data.length <= 1) return []; // Se só tiver cabeçalho ou for vazia

  const headers = data[0];
  const rows = data.slice(1);

  // Mapeia as linhas transformando em Objetos (JSON)
  return rows.map(row => {
    let obj = {};
    headers.forEach((header, index) => {
      obj[header] = row[index];
    });
    return obj;
  });
}
```
</details>

---

## 💾 Como Exportar os Gráficos

O sistema foi desenhado para utilizar a exportação nativa e segura do seu navegador:
1. Clique no botão de **"Mostrar Números" (ícone de olho)** no menu superior direito para exibir os valores absolutos sobre as barras e fatias.
2. Clique com o botão direito do mouse sobre o gráfico desejado e selecione **"Salvar imagem como..."**.
3. A imagem será baixada em formato PNG de alta qualidade.

---

## 📋 Estrutura Exigida no Formulário (Forms)

O script busca palavras-chave específicas no cabeçalho da planilha (geradas pelas perguntas do Google Forms) para cruzar os dados. O cabeçalho deve conter obrigatoriamente as seguintes raízes:

| Informação Desejada | Palavra-chave obrigatória no cabeçalho | Exemplo de Pergunta no Forms |
| :--- | :--- | :--- |
| **Data** | `Data de Atendimento` ou `Carimbo de data` | *Data de Atendimento* |
| **Idade** | `IDADE` | *Qual a sua idade?* |
| **Gênero/Sexo** | `SEXO` | *Sexo / Gênero* |
| **Município** | `MUNICÍPIO` | *Município de Residência* |
| **Tipo de Usuário** | `Tipo de usuário` | *Tipo de usuário dos serviços (PF ou PJ)?* |
| **Conclusão** | `conclusivo` | *O atendimento prestado foi conclusivo?* |
| **Volume de Folhas**| `folhas` | *Se houver, quantas folhas foram impressas?* |
| **Serviços Prestados** | `Tipo de Atendimento` | *Tipo de Atendimento (Múltipla escolha)* |
| **Serviço "Outros"** | `respondeu outro` | *Se respondeu outro, especifique aqui:* |

**Regras Essenciais:**
1. A pergunta de **Tipo de Atendimento** deve ser de Múltipla Escolha (Caixas de seleção).
2. A coluna de **Idade** deve receber apenas números (o painel calcula a média dinamicamente).
3. Na coluna de **Folhas Impressas**, o sistema extrairá apenas o maior número digitado na célula, ignorando textos (ex: "Foram 5 folhas" é lido como `5`).

---

## 📚 Dicionário de Categorização

Como os formulários podem conter preenchimentos manuais não padronizados, o sistema utiliza um algoritmo de varredura para agrupar as demandas em **6 macro categorias principais**. Se nenhum termo for encontrado, a demanda cai em "Outros", que possui uma visualização de "Drill-down" exclusiva na aba Operacional.

| Categoria Final Dashboard | Palavras-chave mapeadas pelo código |
| :--- | :--- |
| **DASN MEI** | DASN, DECLARAÇÃO ANUAL, FATURAMENTO MEI |
| **Parcelamento** | PARCELAMENTO, PARCELA, DIVIDIR, NEGOCIAÇÃO |
| **Imposto de Renda** | IRPF, DIRPF, AJUSTE ANUAL, DECLARAÇÃO DE AJUSTE, RENDIMENTO, RESTITUIÇÃO, IR |
| **Emissão de DARF** | DARF, GUIA, PAGAMENTO |
| **Abertura de MEI** | ABERTURA, ABRIR, FORMALIZAÇÃO, MEI, ABERTURA DE MEI |
| **Outros** | Qualquer entrada que não contenha os termos acima. Agrupamento dinâmico na Aba 2. |

---

## 🛠️ Stack Tecnológica

* **Interface e Estilização:** HTML5, CSS3, [Tailwind CSS](https://tailwindcss.com/)
* **Lógica e Dinâmica:** JavaScript (ES6+) Vanilla
* **Data Parsing Offline:** [PapaParse](https://www.papaparse.com/)
* **Backend em Nuvem:** Google Apps Script (V8)
* **Visualização de Dados:** [Chart.js](https://www.chartjs.org/) + `chartjs-plugin-datalabels`