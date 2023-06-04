class AFD:
    def __init__(self):
        self.estados = []
        self.alfabeto = []
        self.estado_inicial = None
        self.estados_finais = []

    def adicionar_estado(self, estado):
        self.estados.append(estado)

    def adicionar_transicao(self, estado_origem, simbolo, estado_destino):
        for estado in self.estados:
            if estado.nome == estado_origem:
                estado.adicionar_transicao(simbolo, estado_destino)
                return
        raise ValueError(f"O estado '{estado_origem}' não foi encontrado no AFD.")

    def definir_estado_inicial(self, estado):
        self.estado_inicial = estado

    def adicionar_estado_final(self, estado):
        self.estados_finais.append(estado)

class Token:
    def __init__(self, nome):
        self.nome = nome

class GramaticaRegular:
    def __init__(self, nome, producoes):
        self.nome = nome
        self.producoes = producoes

class Transicao:
    def __init__(self, simbolo, estado_destino):
        self.simbolo = simbolo
        self.estado_destino = estado_destino

class Estado:
    def __init__(self, nome, transicoes):
        self.nome = nome
        self.transicoes = transicoes

class AFND:
    def __init__(self):
        self.estados = []
        self.alfabeto = []
        self.estado_inicial = None
        self.estados_finais = []

    def adicionar_estado(self, estado):
        self.estados.append(estado)

    def adicionar_estado_final(self, estado_final):
        self.estados_finais.append(estado_final)

    def adicionar_transicao(self, estado_origem, simbolo, estado_destino):
        for estado in self.estados:
            if estado.nome == estado_origem:
                estado.transicoes.append(Transicao(simbolo, estado_destino))

    def processar_entrada(self, entrada):
        estado_atual = self.estado_inicial
        for simbolo in entrada:
            prox_estado = None
            for estado in self.estados:
                if estado.nome == estado_atual:
                    for transicao in estado.transicoes:
                        if transicao.simbolo == simbolo:
                            prox_estado = transicao.estado_destino
                            break
                    break
            if prox_estado is None:
                return "Rejeitado"
            estado_atual = prox_estado

        if estado_atual in self.estados_finais:
            return "Aceito"
        else:
            return "Rejeitado"


# Função para ler o arquivo de entrada e construir o AFND
def construir_afnd(arquivo_entrada):
    afnd = AFND()
    with open(arquivo_entrada, 'r') as arquivo:
        tokens = []
        grs = []
        linha_atual = None
        for linha in arquivo:
            linha = linha.strip()
            if linha.startswith('tokens:'):
                linha_atual = 'tokens'
                continue
            elif linha.startswith('grs:'):
                linha_atual = 'grs'
                continue

            if linha_atual == 'tokens':
                tokens.append(Token(linha))
            elif linha_atual == 'grs':
                if linha.startswith('<'):
                    nome_gr = linha.strip()
                    producoes = []
                    for linha_gr in arquivo:
                        linha_gr = linha_gr.strip()
                        if linha_gr.startswith('<'):
                            break
                        producoes.append(linha_gr)
                    grs.append(GramaticaRegular(nome_gr, producoes))

        for token in tokens:
            afnd.adicionar_estado(Estado(token.nome, []))
            afnd.adicionar_estado_final(token.nome)
            for simbolo in token.nome:
                afnd.adicionar_transicao(token.nome, simbolo, token.nome)

        for gr in grs:
            afnd.adicionar_estado(Estado(gr.nome, []))
            for producao in gr.producoes:
                simbolos = producao.split('::=')
                if len(simbolos) == 2:
                    estado_origem = gr.nome
                    estado_destino = simbolos[1].strip() + ',' + gr.nome
                    afnd.adicionar_transicao(estado_origem, simbolos[0].strip(), estado_destino)
    
   # print(afnd.estados)
    #print(afnd.alfabeto)
    #print(afnd.estado_inicial)
    #print(afnd.estados_finais)

    return afnd



# Função para determinizar o AFND e obter o AFD



# Função para minimizar o AFD
# Função para determinizar o AFND e obter o AFD
def determinizar_afnd(afnd):
    estado_inicial_afd = frozenset({afnd.estado_inicial})
    estados_afd = [estado_inicial_afd]
    fila = [estado_inicial_afd]

    while fila:
        estado_atual = fila.pop(0)

        for simbolo in afnd.alfabeto:
            conjunto_destino = set()
            for estado in estado_atual:
                for transicao in estado.transicoes:
                    if transicao.simbolo == simbolo:
                        conjunto_destino.add(transicao.estado_destino)

            if conjunto_destino:
                novo_estado = frozenset(conjunto_destino)
                if novo_estado not in estados_afd:
                    estados_afd.append(novo_estado)
                    fila.append(novo_estado)

                estado_origem = ','.join(estado_atual)
                estado_destino = ','.join(novo_estado)
                afnd.adicionar_transicao(estado_origem, simbolo, estado_destino)

    # Definir estados finais do AFD
    for estado_afd in estados_afd:
        for estado in estado_afd:
            if estado in afnd.estados_finais:
                afnd.adicionar_estado_final(','.join(estado_afd))
                break

    print(afnd.estados)
    print(afnd.alfabeto)
    print(afnd.estado_inicial)
    print(afnd.estados_finais)

    return afnd

def verificar_similaridade_estados(estado1, estado2, afd):
    for simbolo in afd.alfabeto:
        proximo_estado1 = afd.obter_proximo_estado(estado1, simbolo)
        proximo_estado2 = afd.obter_proximo_estado(estado2, simbolo)

        if proximo_estado1 != proximo_estado2:
            return False

    return True



# Função para minimizar o AFD
def minimizar_afd(afd):
    # Criação da tabela de marcação
    tabela = [[False] * len(afd.estados) for _ in range(len(afd.estados))]

    # Marcar estados finais e não finais
    for i in range(len(afd.estados)):
        for j in range(i + 1, len(afd.estados)):
            estado1_nome = afd.estados[i].nome
            estado2_nome = afd.estados[j].nome

            if (estado1_nome in afd.estados_finais and estado2_nome not in afd.estados_finais) or (
                    estado2_nome in afd.estados_finais and estado1_nome not in afd.estados_finais):
                tabela[i][j] = True

    # Marcar estados distintos
    for i in range(len(afd.estados)):
        for j in range(i + 1, len(afd.estados)):
            if not tabela[i][j]:
                estado1_nome = afd.estados[i].nome
                estado2_nome = afd.estados[j].nome
                if verificar_similaridade_estados(estado1_nome, estado2_nome, afd):
                    tabela[i][j] = True

    # Dividir estados em partições
    particoes = [set(), set()]
    for i in range(len(afd.estados)):
        if afd.estados[i].nome in afd.estados_finais:
            particoes[1].add(afd.estados[i].nome)
        else:
            particoes[0].add(afd.estados[i].nome)

    # Algoritmo de particionamento
    while True:
        nova_particao = []
        for particao in particoes:
            for simbolo in afd.alfabeto:
                novas_particoes = []

                for estado in particao:
                    proximo_estado = afd.obter_proximo_estado(estado, simbolo)
                    particao_atual = None
                    for p in nova_particao:
                        if proximo_estado in p:
                            particao_atual = p
                            break

                    if particao_atual is None:
                        particao_atual = set()
                        nova_particao.append(particao_atual)

                    particao_atual.add(estado)

                if len(nova_particao) > len(particoes):
                    particoes = nova_particao
                    break
            else:
                continue
            break
        else:
            break

    # Criação do AFD mínimo
    afd_min = AFD()
    estados_afd_min = []
    estado_inicial_afd_min = None
    estados_finais_afd_min = []

    for particao in particoes:
        estado_nome = ','.join(particao)
        estados_afd_min.append(estado_nome)

        if afd.estado_inicial in particao:
            estado_inicial_afd_min = estado_nome

        if any(estado in afd.estados_finais for estado in particao):
                        estados_finais_afd_min.append(estado_nome)

    # Adicionar estados ao AFD mínimo
    for estado_nome in estados_afd_min:
        afd_min.adicionar_estado(Estado(estado_nome, []))


    # Definir estado inicial do AFD mínimo
    afd_min.definir_estado_inicial(estado_inicial_afd_min)

    # Definir estados finais do AFD mínimo
    for estado_nome in estados_finais_afd_min:
        afd_min.adicionar_estado_final(estado_nome)

    # Adicionar transições ao AFD mínimo
    for i in range(len(estados_afd_min)):
        estado_afd_min = estados_afd_min[i]
        for simbolo in afd.alfabeto:
            proximo_estado_afd_min = afd.obter_proximo_estado(','.join(particoes[i]), simbolo)
            afd_min.adicionar_transicao(estado_afd_min, simbolo, proximo_estado_afd_min)

    #print(afd_min.estados)
    #print(afd_min.alfabeto)
    #print(afd_min.estado_inicial)
    #print(afd_min.estados_finais)
    return afd_min



# Função para salvar o AFD em um arquivo de saída
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
