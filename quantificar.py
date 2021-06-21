#!/usr/bin/env python3

"""Quantificador de cores de imagens utilizando algoritmos de busca local"""

import sys, buscas
from problemas import ProblemaQuantificacao
from PIL import Image
from scipy import misc
from sklearn.cluster import KMeans


__author__ = "Nome do aluno"
__copyright__ = "Copyleft"
__credits__ = ["Ricardo Inácio Álvares e Silva"]
__license__ = "GPLv3"
__version__ = "1.0"
__maintainer__ = "Ricardo Inácio Álvares e Silva"
__email__ = "ricardo.silva@unifil.br"
__status__ = "Desenvolvimento"


def quantificar_subida_encosta(**kwargs):
    """
    Funcao que inicializa estruturas de dados e invoca algoritmo de busca local
    por subida de encosta.
    """
    problema = ProblemaQuantificacao(cores, pixels, largura, altura)
    ### Após iniciar estruturas de dados, remova o comentario da linha abaixo
    estado, avaliacoes = buscas.subida_encosta(problema, problema.estado)

    for i in range(largura):
        for j in range(altura):
            pixel = pixels[i,j]
            melhor = estado[0]
            for cor in estado:
                if problema.avaliar_cor(pixel, cor) < problema.avaliar_cor(pixel, melhor):
                    melhor = cor
            
            pixels[i,j] = melhor


def quantificar_feixe_local(**kwargs):
    """
    Funcao que inicializa estruturas de dados e invoca algoritmo de busca em
    feixe local.
    """
    problema = ProblemaQuantificacao(cores, pixels, largura, altura)
    k = argumento
    ### Após iniciar estruturas de dados, remova o comentario da linha abaixo
    estado = buscas.feixe_local(problema, k)

    for i in range(largura):
        for j in range(altura):
            pixel = pixels[i,j]
            melhor = estado[0]
            for cor in estado:
                if problema.avaliar_cor(pixel, cor) < problema.avaliar_cor(pixel, melhor):
                    melhor = cor
            
            pixels[i,j] = melhor

def quantificar_geneticamente(**kwargs):
    """
    Funcao que inicializa estruturas de dados e invoca algoritmo de busca local
    por por algoritmo genético.
    """
    problema = ProblemaQuantificacao(cores, pixels, largura, altura)
    populacao = problema.gerar_estados_iniciais(argumento)
    ### Após iniciar estruturas de dados, remova o comentario da linha abaixo
    resultado = buscas.busca_genetica(populacao, problema.avaliacao)

    for i in range(largura):
        for j in range(altura):
            pixel = pixels[i,j]
            melhor = resultado[0]
            for cor in resultado:
                if problema.avaliar_cor(pixel, cor) < problema.avaliar_cor(pixel, melhor):
                    melhor = cor
            
            pixels[i,j] = melhor


def quantificar_k_medias(**kwargs):
    problema = ProblemaQuantificacao(cores, pixels, largura, altura)
    kmeans = KMeans(n_clusters = argumento)

    colors = []
    for i in range(largura):
        for j in range(altura):
            colors.append(pixels[i,j])

    kmeans.fit(colors)

    centroids = kmeans.cluster_centers_.astype(int)
    labels = kmeans.labels_

    for i in range(largura):
        for j in range(altura):
            pixel = pixels[i,j]
            melhor = tuple(centroids[0])
            for cor in centroids:
                cor = tuple(cor)
                if problema.avaliar_cor(pixel, cor) < problema.avaliar_cor(pixel, melhor):
                    melhor = cor
            
            pixels[i,j] = melhor

if __name__ == "__main__":
    # Leitura e verificacao dos argumentos de linha de comando
    if len(sys.argv) < 5:
        print("Modo de usar: python3 quantificar.py algoritmo argumento cores imagem\n"
            + "algoritmo: nome do algoritmo a ser utilizado\n"
            + "argumento: valor de 'k' para feixe local ou tamanho da populacao\n"
            + "cores: quantidade de cores (número)\n"
            + "imagem: caminho e nome do arquivo com a imagem a ser processada.") 
        exit() 
    
    algoritmo = sys.argv[1]
    argumento = int(sys.argv[2])
    cores = int(sys.argv[3])
    nome_arquivo = sys.argv[4]


    # Define algoritmo a ser aplicado
    if algoritmo == "subida":
        algoritmo = quantificar_subida_encosta
    elif algoritmo == "feixe":
        algoritmo = quantificar_feixe_local
    elif algoritmo == "genetico":
        algoritmo = quantificar_geneticamente
    elif algoritmo == 'kmedias':
        algoritmo = quantificar_k_medias
    else:
        print("Algoritmo especificado inválido: {0}".format(algoritmo))
        print("Algoritmos válidos são: {0}, {1}, {2}, {3}"
              .format("subida", "feixe", "genetico", "kmedias"))
        exit()
        
    
    if cores < 1:
        print("Quantidade de cores pós-quantizacão deve ser no mínimo 1.")
        exit()
    
    # Abrir a imagem especificada
    try:
        original = Image.open(nome_arquivo)
    except IOError as err:
        print("Erro ao acessar arquivo: {0}".format(err))
    
    # Copiar imagem para poder comparar ambas ao final.    
    reduzida = original.copy()
    
    # Obtendo acesso aos pixels da cópia. Cada posicao é uma tupla (R, G, B)
    # R, G e B tem domínio em [0,255], ou seja, 0 <= x <= 255
    pixels = reduzida.load()
    largura, altura = reduzida.size

    algoritmo(reduzida=reduzida, argumento=argumento, cores=cores, pixels=pixels, largura=largura, altura=altura)
    
    original.show()
    reduzida.show()
    reduzida.save(nome_arquivo.split(".")[0] + "-final.png")
    
    exit()

else:
    raise ImportError("Este módulo só pode funcionar como o principal.")