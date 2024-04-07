import pandas as pd
import csv
import os
import shutil

# Definindo o delimitador usado nos arquivos CSV
DELIMITADOR = ';'
# Definindo o caminho para o arquivo temporário
ARQUIVO_TEMPORARIO = 'dadosLoja_temp.csv'

# Função para corrigir problemas de formatação
def corrigir_linha_problematica(caminho_arquivo_origem, caminho_arquivo_destino):
    """Corrige uma linha problemática no arquivo CSV."""
    with open(caminho_arquivo_origem, 'r', encoding='utf-8') as arquivo_origem:
        with open(caminho_arquivo_destino, 'w', encoding='utf-8', newline='') as arquivo_destino:
            leitor_csv = csv.reader(arquivo_origem, delimiter=DELIMITADOR)
            escritor_csv = csv.writer(arquivo_destino, delimiter=DELIMITADOR)
            for i, linha in enumerate(leitor_csv):
                if i == 19:
                    linha_corrigida = DELIMITADOR.join(linha)
                    escritor_csv.writerow([linha_corrigida])
                else:
                    escritor_csv.writerow(linha)

def filtrar_por_tamanho_codigo_de_barras(dados_filtrados):
    """Separa os dados em duas tabelas com base no tamanho do código de barras."""
    dados_filtrados['tamanho_codigo_de_barras'] = dados_filtrados['cod_produto'].astype(str).apply(len)
    dados_menor_13 = dados_filtrados[dados_filtrados['tamanho_codigo_de_barras'] < 13]
    dados_maior_13 = dados_filtrados[dados_filtrados['tamanho_codigo_de_barras'] >= 13]
    dados_filtrados = dados_filtrados.drop(columns=['tamanho_codigo_de_barras'])
    return dados_menor_13, dados_maior_13

def formatar_quantidade(dados):
    """Formata a coluna 'quantidade' para números inteiros."""
    # Substituir valores não finitos por NaN
    dados['quantidade'] = pd.to_numeric(dados['quantidade'], errors='coerce')
    # Substituir NaN por 0
    dados['quantidade'] = dados['quantidade'].fillna(0)
    # Converter para inteiro
    dados['quantidade'] = dados['quantidade'].astype(int)
    return dados

def salvar_tabelas(dados_menor_13, dados_maior_13):
    """Salva as tabelas com os registros de códigos de barras menores e maiores de 13 dígitos."""
    dados_menor_13.to_csv('dadosMenor13.csv', index=False, sep=DELIMITADOR, quoting=csv.QUOTE_NONNUMERIC)
    dados_maior_13.to_csv('dadosMaior13.csv', index=False, sep=DELIMITADOR, quoting=csv.QUOTE_NONNUMERIC)
    print("As tabelas com os registros de códigos de barras menores e maiores de 13 dígitos foram salvas.")

def ler_dados_loja(caminho_arquivo_origem):
    """Lê os dados da loja do arquivo CSV."""
    # Copiar o arquivo original para não modificar
    shutil.copyfile(caminho_arquivo_origem, ARQUIVO_TEMPORARIO)

    # Corrigir o arquivo CSV, se necessário
    corrigir_linha_problematica(caminho_arquivo_origem, ARQUIVO_TEMPORARIO)

    # Abrir a planilha e ler os dados
    dados = pd.read_csv(ARQUIVO_TEMPORARIO, delimiter=DELIMITADOR)

    # Substituir pontos por vírgulas nas colunas E e F
    dados['preco_custo'] = dados['preco_custo'].astype(str).str.replace('.', ',')
    dados['preco_venda'] = dados['preco_venda'].astype(str).str.replace('.', ',')

    # Formatar a coluna 'quantidade'
    dados = formatar_quantidade(dados)

    # Filtrar a tabela pela coluna "quantidade"
    dados_filtrados = dados[dados['quantidade'] > 0]

    # Identificar as linhas com quantidade 0 ou negativa e removê-las
    dados_removidos = dados[dados['quantidade'] <= 0]

    # Salvar as tabelas filtradas em novos arquivos CSV
    dados_filtrados.to_csv('dadosFiltrados.csv', index=False, sep=DELIMITADOR, quoting=csv.QUOTE_NONNUMERIC)
    dados_removidos.to_csv('dadosRemovidos.csv', index=False, sep=DELIMITADOR, quoting=csv.QUOTE_NONNUMERIC)

    # Filtrar os dados por tamanho do código de barras
    dados_menor_13, dados_maior_13 = filtrar_por_tamanho_codigo_de_barras(dados_filtrados)

    # Salvar as tabelas com os registros de códigos de barras menores e maiores de 13 dígitos
    salvar_tabelas(dados_menor_13, dados_maior_13)

    # Remover o arquivo temporário
    os.remove(ARQUIVO_TEMPORARIO)

if __name__ == "__main__":
    # Caminho para o arquivo CSV original
    caminho_arquivo = 'dadosLoja.csv'

    # Chamar a função para ler os dados da loja
    ler_dados_loja(caminho_arquivo)
