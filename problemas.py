#!/usr/bin/env python3

"""Módulo com implementacao da modelagem do problema abordado"""

__author__ = "Nome do aluno"
__copyright__ = "Copyleft"
__credits__ = ["Ricardo Inácio Álvares e Silva"]
__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Aluno"
__email__ = "seu@email.com"
__status__ = "Desenvolvimento"

from math import sqrt
import random

class ProblemaLocal():
    """Classe abstrata com interfaces para implementacao de busca local"""
    
    def __init__(self, s):
        self.estado_inicial = s
    
    def heuristica(self, s):
        raise NotImplementedError()
    
    def acoes(self, s):
        raise NotImplementedError()
    
    def resultado(self, s, a):
        raise NotImplementedError()


class ProblemaQuantificacao(ProblemaLocal):
    """Aqui você implementará a modelagem da busca local em quantizacao de
    imagens"""
    
    def __init__(self, cores, pixels, largura, altura):
        self.cores = cores
        self.estado = self.estado()
        self.pixels = pixels
        self.largura = largura
        self.altura = altura
    
    def estado(self):
        paleta = []  
        for _ in range(self.cores):
            random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            paleta.append(random_color)

        return paleta

    def get_adjacentes(self, estado) :
        adjacentes = []
        for i in range(len(estado)):
            tupla = estado[i]
            novo_adjacente = estado.copy()
            for j in range(len(tupla)):
                lista_tupla = list(tupla)
                lista_tupla[j] += 1
                nova_tupla = tuple(lista_tupla)
                novo_adjacente[i] = nova_tupla
                adjacentes.append(novo_adjacente)
                novo_adjacente = estado.copy()
            
            for j in range(len(tupla)):
                lista_tupla = list(tupla)
                lista_tupla[j] -= 1
                nova_tupla = tuple(lista_tupla)
                novo_adjacente[i] = nova_tupla
                adjacentes.append(novo_adjacente)
                novo_adjacente = estado.copy()

        return adjacentes

    def avaliacao(self, estado):

        hist = {}
        for i in range(self.largura):
                for h in range(self.altura):
                    hist[self.pixels[i,h]] = hist.get(self.pixels[i,h], 0) + 1
        distancia_euclidiana = 0
        for cor in estado:
            for pixel in hist:
                distancia_atual = abs(pixel[0] - cor[0]) + abs(pixel[1] - cor[1]) + abs(pixel[2] - cor[2]) * hist[pixel]
                distancia_euclidiana += distancia_atual
        
        return distancia_euclidiana

    def avaliar_cor(self, pixel, cor):
        return sqrt((pixel[0] - cor[0]) ** 2 + (pixel[1] - cor[1]) ** 2 + (pixel[2] - cor[2]) ** 2)

    def gerar_estados_iniciais(self, n):
        estados = []
        for _ in range(n):
            paleta = []
            for _ in range(self.cores):
                random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                paleta.append(random_color)
            
            estados.append(paleta)

        return estados


if __name__ == "__main__":
    print("Este módulo não deve ser utilizado como o principal ou inicial")
    exit()