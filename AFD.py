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