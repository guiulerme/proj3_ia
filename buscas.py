#!/usr/bin/env python3

"""Módulo que abriga os algoritmos de quantificacao de imagens"""

__author__ = "Nome do aluno"
__copyright__ = "Copyleft"
__credits__ = ["Ricardo Inácio Álvares e Silva"]
__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Aluno"
__email__ = "seu@email.com"
__status__ = "Desenvolvimento"

import random

def subida_encosta(problema, estado):
    """
    Busca local por subida de encosta.
    
    :param problema: objeto da classe ProblemaLocal
    :return: estado final de um pico do problema (global ou local).
    """
    avaliacoes = []
    contador = 0
    parar = 0

    while True:
        adjacentes = problema.get_adjacentes(estado)
        atual = problema.avaliacao(estado)
        melhor = atual
        estado_atual = problema.estado
        avaliacoes.append(atual)

        for adjacente in adjacentes:
            avaliacao = problema.avaliacao(adjacente)
            
            if avaliacao <= melhor:
                parar += 1 if avaliacao == melhor else 0
                melhor = avaliacao
                estado = adjacente

        contador += 1
        if melhor == atual and estado_atual == estado or parar == 20:
            break

    return estado, avaliacoes

def feixe_local(problema, k):
    """
    Busca por feixe local.
    
    :param problema: objeto da classe ProblemaLocal
    :param k: quantidade de estados a passarem de uma geracão à outra
    :return: estado final de um pico do problema (global ou local).
    """
    estados_iniciais = problema.gerar_estados_iniciais(k)

    k_atuais = estados_iniciais

    while True:
        k_adjacentes = list()
        for k_atual in k_atuais:
            k_adjacentes += list(problema.get_adjacentes(k_atual))
        
        k_adjacentes.sort(key=lambda estado: problema.avaliacao(estado))

        if problema.avaliacao(k_adjacentes[0]) > problema.avaliacao(k_atuais[0]):
            k_atuais = k_adjacentes[:k]
        else:
            return k_atuais[0]

def busca_genetica(populacao, fn_fitness):
    """
    Busca local por algoritmo genético.
    
    :param populacao: lista de strings, cada string são os "genes" de um individuo
    :param fn_fitness: funcao capaz de avaliar a qualidade de um individuo
    :return: um individuo com a funcao_fitness desejada
    """    
    
    geracao_atual = populacao

    def gerar_cor():
        return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

    while True:
        fitnesses = []
        for cromossomo in geracao_atual:
            avaliacao = fn_fitness(cromossomo)
            fitnesses.append(avaliacao)
        fitness_populacao = sum(fitnesses)
        fitnesses_weights = [fn_fitness(e)/fitness_populacao for e in geracao_atual]

        prox_ger = random.choices(geracao_atual, fitnesses_weights, k=len(geracao_atual))

        for n in range(0, len(prox_ger), 2):
            macho, femea = prox_ger[n], prox_ger[n+1]
            index = random.randint(0,len(macho) - 1)
            for i in range(index, len(macho)):
                copia = macho[i]
                macho[i] = femea[i]
                femea[i] = copia

        alpha = 0.1
        for i in range(len(prox_ger)):
            for j in range(len(prox_ger[i])):
                prox_ger[i][j] = gerar_cor() if random.random() < alpha else prox_ger[i][j]

        geracao_atual.sort(key=lambda estado: fn_fitness(estado))

        if (fn_fitness(prox_ger[0]) > fn_fitness(geracao_atual[0])):
            geracao_atual = prox_ger
        else:
            return geracao_atual[0]

if __name__ == "__main__":
    print("Este módulo não deve ser utilizado como o principal ou inicial")
    exit()
