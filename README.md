# 📊 Dashboard Analítico NAF (Núcleo de Apoio Contábil e Fiscal)

Dashboard interativo desenvolvido em Single Page Application (SPA) para analisar e visualizar os dados de atendimentos registrados nas planilhas do NAF. 

A ferramenta foi construída com foco em **segurança e conformidade com a LGPD**, realizando o processamento, limpeza e cruzamento dos dados de forma 100% local (Client-side) no navegador do usuário, sem envio de informações para servidores externos.

## ✨ Principais Funcionalidades

- **Processamento Local (PapaParse):** Leitura instantânea de arquivos CSV diretamente no navegador.
- **Higienização de Dados:** Padronização automática de strings (conversão para maiúsculas, remoção de espaços extras) para evitar duplicidade na contagem das categorias.
- **Desmembramento de Atendimentos Múltiplos:** Identifica quando um único usuário seleciona múltiplos serviços em um único formulário e contabiliza a volumetria de serviços de forma correta, sem distorcer o número total de pessoas físicas atendidas.
- **Filtros Dinâmicos Multi-nível:** Análise granular através de filtros combinados: `Ano`, `Mês`, `Município`, `Público` (PF/PJ), `Faixa Etária`, `Gênero` e `Status de Conclusão`.
- **Análise de Desigualdade de Gênero:** Visualização dedicada e filtrada exclusivamente para mensurar a proporção entre os gêneros Masculino e Feminino nas solicitações de Imposto de Renda.
- **Filtro para Folhas Impressas:** A ferramenta sempre pegará o maior valor da coluna `Se houver, quantas folhas foram impressas:`. Isso impede que células com `ate`ou com vírgula sejam preenchidas incorretamente.

## 📝 Como Estruturar o Google Forms e o Google Sheets

Para que o dashboard funcione corretamente e o código consiga localizar os dados automaticamente, as perguntas no seu Google Forms (que geram o cabeçalho da planilha) devem conter **palavras-chave específicas**.

A aplicação faz uma busca flexível pelos cabeçalhos, mas é estritamente necessário que as colunas contenham os seguintes termos na primeira linha (cabeçalho) do CSV:

| Informação Desejada | Palavra-chave obrigatória no cabeçalho da planilha | Exemplo de Pergunta no Forms |
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

### Regras do Formulário:
1. A pergunta de **Tipo de Atendimento** deve permitir **múltiplas seleções** (Caixas de seleção), caso a pessoa busque mais de um serviço no mesmo dia.
2. A coluna de Idade deve receber preferencialmente números exatos. O script agrupará as idades em **Faixas Etárias** automaticamente.

### Como Exportar os Dados:
1. Abra o Google Sheets vinculado ao seu Google Forms.
2. Acesse: **Arquivo > Fazer download > Valores separados por vírgulas (.csv)**.
3. Certifique-se de que o sistema operacional / Google Sheets exporte utilizando o padrão nacional com delimitador por ponto e vírgula (`;`). Caso o delimitador esteja como vírgula (`,`), utilize o [Libreoffice Calc](https://pt-br.libreoffice.org/), salve como .csv escolha o delimitador ponto e vírgula (`;`).
4. Importe o arquivo baixado diretamente no botão "Carregar CSV" do Dashboard.

## 🗂️ Dicionário de Categorização e Hierarquia

Como os formulários podem conter preenchimentos manuais não padronizados e descrições longas, o sistema utiliza um algoritmo de varredura (da regra mais específica para a mais geral) para agrupar as demandas em **6 macros categorias principais**.

```javascript
const categoriasDicionario = {
    "DASN MEI": ["DASN", "DECLARAÇÃO ANUAL", "FATURAMENTO MEI"],
    "Parcelamento": ["PARCELAMENTO", "PARCELA", "DIVIDIR", "NEGOCIAÇÃO"],
    "Imposto de Renda": ["IRPF", "DIRPF", "AJUSTE ANUAL", "DECLARAÇÃO DE AJUSTE", "RENDIMENTO", "RESTITUIÇÃO", "IR"],
    "Emissão de DARF": ["DARF", "GUIA", "PAGAMENTO"],
    "Abertura de MEI": ["ABERTURA", "ABRIR", "FORMALIZAÇÃO", "MEI", "ABERTURA DE MEI"],
    "Outros": []
};
```

| Categoria Final Dashboard | Palavras-chave mapeadas pelo código |
| :--- | :--- |
| **DASN MEI** | DASN, DECLARAÇÃO ANUAL, FATURAMENTO MEI |
| **Parcelamento** | PARCELAMENTO, PARCELA, DIVIDIR, NEGOCIAÇÃO |
| **Imposto de Renda** | IRPF, DIRPF, AJUSTE ANUAL, DECLARAÇÃO DE AJUSTE, RENDIMENTO, RESTITUIÇÃO, IR |
| **Emissão de DARF** | DARF, GUIA, PAGAMENTO |
| **Abertura de MEI** | ABERTURA, ABRIR, FORMALIZAÇÃO, MEI, ABERTURA DE MEI |
| **Outros** | Qualquer entrada que não contenha os termos acima. |

## 🚀 Como Executar Localmente

Não é necessário instalar nenhum servidor ou framework (como Node.js ou Python).
1. Faça o clone ou baixe este repositório.
2. Abra o arquivo `index.html` em qualquer navegador web moderno (Google Chrome, Edge, Firefox, Safari).
3. Faça o upload do arquivo CSV extraído.

## 🛠️ Stack Tecnológica

* **Interface e Estilização:** HTML5, CSS3, [Tailwind CSS](https://tailwindcss.com/)
* **Lógica e Dinâmica:** JavaScript (ES6+) Vanilla
* **Data Parsing:** [PapaParse](https://www.papaparse.com/)
* **Data Visualization:** [Chart.js](https://www.chartjs.org/)