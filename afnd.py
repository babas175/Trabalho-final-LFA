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