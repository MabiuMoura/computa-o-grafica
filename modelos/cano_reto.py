import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import math

def modelar_cano_reto(self, raio_interno, raio_externo, altura, resolucao=32):

    for i in range(resolucao):
        theta = 2 * math.pi * i / resolucao
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)

        x_out = raio_externo * cos_t
        y_out = raio_externo * sin_t
        x_in = raio_interno * cos_t
        y_in = raio_interno * sin_t

        self.vertices.append([x_out, y_out, 0])         # base externa
        self.vertices.append([x_out, y_out, altura])    # topo externa
        self.vertices.append([x_in, y_in, 0])           # base interna
        self.vertices.append([x_in, y_in, altura])      # topo interna

    for i in range(resolucao):
        i1 = i * 4
        i2 = ((i + 1) % resolucao) * 4

        # Lateral externa
        self.faces.append([self.vertices[i1], self.vertices[i2], self.vertices[i2 + 1]])
        self.faces.append([self.vertices[i1], self.vertices[i2 + 1], self.vertices[i1 + 1]])

        # Lateral interna (invertida)
        self.faces.append([self.vertices[i1 + 2], self.vertices[i2 + 3], self.vertices[i2 + 2]])
        self.faces.append([self.vertices[i1 + 2], self.vertices[i1 + 3], self.vertices[i2 + 3]])

        # Tampa inferior
        self.faces.append([self.vertices[i1], self.vertices[i1 + 2], self.vertices[i2 + 2]])
        self.faces.append([self.vertices[i1], self.vertices[i2 + 2], self.vertices[i2]])

        # Tampa superior
        self.faces.append([self.vertices[i1 + 1], self.vertices[i2 + 1], self.vertices[i2 + 3]])
        self.faces.append([self.vertices[i1 + 1], self.vertices[i2 + 3], self.vertices[i1 + 3]])

    return self.vertices, self.faces