import pandas as pd
import csv
import os
import shutil

# Função para corrigir problemas de formatação
def corrigir_linha_problematica(caminho_arquivo_origem, caminho_arquivo_destino):
    with open(caminho_arquivo_origem, 'r', encoding='utf-8') as arquivo_origem:
        with open(caminho_arquivo_destino, 'w', encoding='utf-8', newline='') as arquivo_destino:
            leitor_csv = csv.reader(arquivo_origem, delimiter=';')
            escritor_csv = csv.writer(arquivo_destino, delimiter=';')
            for i, linha in enumerate(leitor_csv):
                # Se for a linha problemática (linha 20 no exemplo), tentamos corrigi-la
                if i == 19:
                    # Juntar os campos com uma vírgula e substituir a linha problemática
                    linha_corrigida = ';'.join(linha)
                    escritor_csv.writerow([linha_corrigida])
                else:
                    escritor_csv.writerow(linha)

def ler_dados_loja(caminho_arquivo_origem):
    # Copiar o arquivo original para não modificar
    caminho_arquivo_temporario = 'dadosLoja_temp.csv'
    shutil.copyfile(caminho_arquivo_origem, caminho_arquivo_temporario)

    # Corrigir o arquivo CSV, se necessário
    corrigir_linha_problematica(caminho_arquivo_origem, caminho_arquivo_temporario)

    # Passo 1: Abrir a planilha e ler os dados
    dados = pd.read_csv(caminho_arquivo_temporario, delimiter=';')

    # Passo 2: Substituir pontos por vírgulas nas colunas E e F
    dados['preco_custo'] = dados['preco_custo'].astype(str).str.replace('.', ',')
    dados['preco_venda'] = dados['preco_venda'].astype(str).str.replace('.', ',')

    # Passo 3: Filtrar a tabela pela coluna "quantidade"
    dados_filtrados = dados[dados['quantidade'] > 0]

    # Passo 4: Identificar as linhas com quantidade 0 ou negativa e removê-las
    dados_removidos = dados[dados['quantidade'] <= 0]

    # Salvar as tabelas filtradas em novos arquivos CSV com alinhamento à esquerda
    dados_filtrados.to_csv('dadosFiltrados.csv', index=False, sep=';', quoting=csv.QUOTE_NONNUMERIC)
    dados_removidos.to_csv('dadosRemovidos.csv', index=False, sep=';', quoting=csv.QUOTE_NONNUMERIC)

    print("As tabelas filtradas foram salvas nos arquivos 'dadosFiltrados.csv' e 'dadosRemovidos.csv'.")

    # Remover o arquivo temporário
    os.remove(caminho_arquivo_temporario)

if __name__ == "__main__":
    # Caminho para o arquivo CSV original
    caminho_arquivo = 'dadosLoja.csv'

    # Chamar a função para ler os dados da loja
    ler_dados_loja(caminho_arquivo)
