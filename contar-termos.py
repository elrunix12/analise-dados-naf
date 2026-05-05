import pandas as pd

# 1. Carrega o arquivo
df = pd.read_csv('NAF - Ficha do Serviço Prestado (respostas) - Respostas ao formulário 1.csv', sep=None, engine='python')

# 2. Define a coluna que você quer analisar
coluna = 'Se respondeu outro, especifique aqui:'

# 3. Tratamento de Choque:
# - Transforma tudo em String
# - Divide por vírgula (split) para separar quem marcou mais de uma opção
# - 'explode' transforma cada item da lista em uma nova linha
# - strip() remove espaços em branco e upper() padroniza
contagem = (
    df[coluna]
    .astype(str)
    .str.split(',')
    .explode()
    .str.strip()
    .str.upper()
    .value_counts()
)

# 4. Exibe o resultado e salva em um novo CSV
print(contagem)
contagem.to_csv('contagem_termos_naf.csv')
