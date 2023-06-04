# Função para salvar o AFD em um arquivo de saída
from afnd import construir_afnd
from afd import determinizar_afnd
from minimizar import minimizar_afd
from tabulate import tabulate



def salvar_afd(afd):
    headers = ["Estado", "Transição"]
    table_data = []

    for estado in afd.estados:
        for transicao in estado.transicoes:
            table_data.append([estado.nome, transicao.simbolo, transicao.estado_destino])

    # Add additional information to the table
    table_data.append(["Estados:", ", ".join(estado.nome for estado in afd.estados)])
    table_data.append(["Estados Finais:", afd.estados_finais])  # Remove the join() method

    print(tabulate(table_data, headers=headers, tablefmt="grid"))


# Função principal para execução do programa
def main():
    arquivo_entrada = "arquivo_entrada.txt"
    # Construir o AFND a partir do arquivo de entrada
    afnd = construir_afnd(arquivo_entrada)
    # Determinizar o AFND para obter o AFD
    afd = determinizar_afnd(afnd)
    # Minimizar o AFD
    afd_min = minimizar_afd(afd)
    # Imprimir o AFD
    salvar_afd(afd_min)
    print('Processamento concluído!')

# Executar o programa
if __name__ == '__main__':
    main()
