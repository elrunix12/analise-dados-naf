# Dashboard Analítico NAF (Núcleo de Apoio Contábil e Fiscal)

Dashboard interativo desenvolvido em Single Page Application (SPA) para analisar e visualizar os dados de atendimentos registrados nas planilhas do NAF. 

A ferramenta foi construída com foco em **segurança e conformidade com a LGPD**, realizando o processamento, limpeza e cruzamento dos dados de forma 100% local (Client-side) no navegador do usuário, sem envio de informações para servidores externos.

## 🚀 Principais Funcionalidades

*   **Processamento Local (PapaParse):** Leitura instantânea de arquivos CSV diretamente no navegador.
*   **Visão em Abas Estruturadas:** Dados segmentados nas visões *Geral*, *Operacional (Serviços)* e *Perfil do Contribuinte* para facilitar a análise.
*   **Higienização de Dados:** Padronização automática de strings (conversão para maiúsculas, remoção de acentos e espaços extras) para evitar duplicidade na contagem das categorias.
*   **Desmembramento de Atendimentos Múltiplos:** Identifica quando um único usuário seleciona múltiplos serviços no formulário e contabiliza a volumetria de forma correta, sem distorcer o número total de pessoas físicas atendidas.
*   **Filtros Dinâmicos Multi-nível:** Análise granular através de filtros combinados globais (`Ano`, `Mês`, `Município`) e locais (`Público`, `Conclusão`, `Serviço`, `Gênero`).
*   **Modo de Rótulos de Dados (Exportação):** Botão integrado (ícone de olho) para ligar/desligar os números exatos nos gráficos, preparando o painel para salvamento rápido de imagens.

## 💾 Como Exportar os Gráficos

O sistema foi desenhado para utilizar a exportação nativa e segura do seu navegador:
1. Clique no botão de **"Mostrar Números" (ícone de olho)** no menu superior direito para exibir os valores absolutos em todos os gráficos.
2. Clique com o botão direito do mouse sobre o gráfico desejado e selecione **"Salvar imagem como..."**.

---

## 📋 Estrutura Exigida no Google Forms/Sheets

Para que o dashboard funcione corretamente, as perguntas no seu Google Forms (que geram o cabeçalho da planilha) devem conter **palavras-chave específicas**. O script busca essas palavras-chave para montar os gráficos.

O arquivo CSV deve conter, obrigatoriamente, em sua primeira linha, as seguintes raízes textuais:

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
1. A pergunta de **Tipo de Atendimento** deve permitir **múltiplas seleções** (Caixas de seleção).
2. A coluna de Idade deve receber números. O script calculará a média e agrupará as idades em **Faixas Etárias** automaticamente.
3. Se preenchido, o sistema extrairá apenas o maior número digitado na pergunta de "folhas impressas" para evitar que descrições em texto quebrem a soma.

### Como Exportar os Dados do Google:
1. Abra o Google Sheets vinculado ao seu Google Forms.
2. Acesse: `Arquivo > Fazer download > Valores separados por vírgulas (.csv)`.
3. Carregue o arquivo baixado diretamente no botão "Carregar" do Dashboard. O sistema tentará detectar o delimitador (vírgula ou ponto e vírgula) automaticamente.

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

## ⚙️ Como Executar Localmente

Não é necessário instalar nenhum servidor ou framework (como Node.js ou Python).

1. Faça o clone ou baixe este repositório.
2. Dê um duplo clique no arquivo `index.html` para abri-lo em qualquer navegador web moderno (Google Chrome, Edge, Firefox).
3. Faça o upload do arquivo `.csv` e inicie a análise.

## 🛠️ Stack Tecnológica

*   **Interface e Estilização:** HTML5, CSS3, [Tailwind CSS](https://tailwindcss.com/)
*   **Lógica e Dinâmica:** JavaScript (ES6+) Vanilla
*   **Data Parsing:** [PapaParse](https://www.papaparse.com/)
*   **Visualização de Dados:** [Chart.js](https://www.chartjs.org/) + `chartjs-plugin-datalabels`