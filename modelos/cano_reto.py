import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import math

def modelar_cano_reto(raio_interno, raio_externo, altura, resolucao=32):
    vertices = []
    faces = []

    for i in range(resolucao):
        theta = 2 * math.pi * i / resolucao
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)

        x_out = raio_externo * cos_t
        y_out = raio_externo * sin_t
        x_in = raio_interno * cos_t
        y_in = raio_interno * sin_t

        vertices.append([x_out, y_out, 0])         # base externa
        vertices.append([x_out, y_out, altura])    # topo externa
        vertices.append([x_in, y_in, 0])           # base interna
        vertices.append([x_in, y_in, altura])      # topo interna

    for i in range(resolucao):
        i1 = i * 4
        i2 = ((i + 1) % resolucao) * 4

        # Lateral externa
        faces.append([vertices[i1], vertices[i2], vertices[i2 + 1]])
        faces.append([vertices[i1], vertices[i2 + 1], vertices[i1 + 1]])

        # Lateral interna (invertida)
        faces.append([vertices[i1 + 2], vertices[i2 + 3], vertices[i2 + 2]])
        faces.append([vertices[i1 + 2], vertices[i1 + 3], vertices[i2 + 3]])

        # Tampa inferior
        faces.append([vertices[i1], vertices[i1 + 2], vertices[i2 + 2]])
        faces.append([vertices[i1], vertices[i2 + 2], vertices[i2]])

        # Tampa superior
        faces.append([vertices[i1 + 1], vertices[i2 + 1], vertices[i2 + 3]])
        faces.append([vertices[i1 + 1], vertices[i2 + 3], vertices[i1 + 3]])

    return vertices, faces