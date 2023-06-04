# Função para salvar o AFD em um arquivo de saída
from afnd import construir_afnd
from afd import determinizar_afnd
from minimizar import minimizar_afd



def salvar_afd(afd):
    print('estados: {}'.format(','.join(estado.nome for estado in afd.estados)))
    print('alfabeto: {}'.format(','.join(afd.alfabeto)))
    print('estado_inicial: {}'.format(afd.estado_inicial))
    print('estados_finais: {}'.format(','.join(estado for estado in afd.estados_finais)))
    print()
    for estado in afd.estados:
        for transicao in estado.transicoes:
            print('{} -{}-> {}'.format(estado.nome, transicao.simbolo, transicao.estado_destino))




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
