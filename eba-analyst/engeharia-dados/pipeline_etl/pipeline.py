###CONTEXTO##
##Análise de Produção de Alimentos e Cálculo de Margem de Lucro

##Você trabalha em uma empresa que se dedica à produção e comercialização de alimentos. A equipe de produção coleta dados diários
# sobre a quantidade de alimentos produzidos, o preço médio de venda e a receita total gerada. Esses daods são armazenados em
# arquivos csv, mas precisam passar por um processo de limpeza, transformação e enriquecimento antes de serem utilizados
# para análise e tomada de decisão.

# O obejtivo é calcular a margem de lucro de cada produto, com base nas informações de receita total, preço médio e quantidade produzida,
# além de garantir que apenas produtos com uma quantidade superior a 10 unidades sejam considerados para análise.

##DESAFIO###
# O analista de dados da empresa foi encarregado de criar uma pipeline de extração, limpeza, transformação e
# enriquecimento desses dados. A primeira etapa consiste em ler o arquivo csv com os dados de
# produção de alimentos, processar e calcular a margem de lucro de cada produto, e então armazenar esses dados
# em um banco de dados SQLite para consultar futuras

##Criação do pipeline
import csv
import sqlite3

# --- CONFIGURAÇÕES E CONSTANTES ---
# Centralizamos os nomes dos arquivos. Se mudar, altera só aqui.
ARQUIVO_FONTE = "producao_alimentos.csv"
NOME_BANCO = "eng_eba.db"


def verificar_tabela(banco_dados, tabela):
    """Função auxiliar para validar se os dados foram salvos corretamente."""
    conn = sqlite3.connect(banco_dados)
    cursor = conn.cursor()

    # ATENÇÃO: O 'f' antes das aspas é obrigatório para usar {tabela}
    cursor.execute(f"SELECT * FROM {tabela}")

    resultados = cursor.fetchall()
    conn.close()
    return resultados


print("Iniciando Pipeline ETL...")

# 1. Abertura do arquivo CSV (EXTRAÇÃO)
with open(ARQUIVO_FONTE, "r", encoding="utf-8") as file:
    reader = csv.reader(file)

    # Pula o cabeçalho para não ler "quantidade" como texto
    next(reader)

    # 2. Conexão com Banco de Dados e Preparação (SCHEMA)
    conn = sqlite3.connect(NOME_BANCO)

    # Limpa a tabela antiga para evitar duplicidade (Idempotência)
    conn.execute("DROP TABLE IF EXISTS producao")

    # Cria a tabela com a estrutura correta
    conn.execute(
        """
        CREATE TABLE producao (
            produto TEXT,
            quantidade REAL,
            preco_medio REAL,
            receita_total REAL,
            custo_kg REAL,
            margem_lucro_porcentagem REAL
        )
    """
    )

    # 3. Processamento linha a linha (TRANSFORMAÇÃO)
    contador = 0
    for row in reader:

        # Mapeamento de variáveis (Facilita a leitura e manutenção)
        produto = row[0]
        quantidade = float(row[1])
        preco_medio = float(row[2])
        receita_total = float(row[3])
        custo_kg = float(row[4])

        # REGRA DE NEGÓCIO 1: Filtrar apenas produções relevantes (> 10)
        if quantidade > 10:

            # REGRA DE NEGÓCIO 2: Cálculo de Margem de Lucro
            # Fórmula: ((Receita - Custo Total) / Receita) * 100
            custo_total = quantidade * custo_kg
            margem_lucro = ((receita_total - custo_total) / receita_total) * 100

            # 4. Carga no Banco (LOAD)
            conn.execute(
                """INSERT INTO producao (
                    produto, quantidade, preco_medio, receita_total, custo_kg, margem_lucro_porcentagem
                ) VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    produto,
                    quantidade,
                    preco_medio,
                    receita_total,
                    custo_kg,
                    margem_lucro,
                ),
            )
            contador += 1

    # Salva as alterações no disco e fecha a conexão
    conn.commit()
    conn.close()

print(f"Pipeline Finalizado! {contador} registros processados e salvos.")

# --- VALIDAÇÃO FINAL ---
print("\nVerificando dados no banco:")
dados = verificar_tabela(NOME_BANCO, "producao")
for linha in dados:
    print(linha)
