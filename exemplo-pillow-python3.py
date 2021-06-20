#!/usr/bin/env python3

"""Exemplo de utilizacao de imagens em python3 com Pillow"""

from PIL import Image

__author__ = "Nome do aluno"
__copyright__ = "Copyleft"
__credits__ = ["python3 wikibooks"]
__license__ = "GPLv3"
__version__ = "1.0"
__maintainer__ = "Ricardo Inácio Álvares e Silva"
__email__ = "ricardo.silva@unifil.br"
__status__ = "Entregue"

if __name__ == "__main__":
    # cria uma nova imagem RGB, toda preta
    img = Image.new( 'RGB', (255,255), "black")

    # cria a matriz de pixels
    pixels = img.load()

    # para cada pixel:
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            # define uma cor (R, G, B)
            pixels[i,j] = (i, j, 100)

    img.show()
    img.save("exemplo.png")
