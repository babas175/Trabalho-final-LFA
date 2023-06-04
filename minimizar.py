




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
