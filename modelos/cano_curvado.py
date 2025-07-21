import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from utils import curva_hermite


def gerar_cano_curvado(P0, P1, T0, T1, raio=0.2, resolucao_circular=16, resolucao_curva=100):
    
    curva = curva_hermite(P0, P1, T0, T1, resolucao_curva)
    vertices = []
    faces = []

    for i in range(resolucao_curva):
        ponto = curva[i]

        # Aproximação da tangente para plano local
        if i < resolucao_curva - 1:
            direcao = curva[i + 1] - curva[i]
        else:
            direcao = curva[i] - curva[i - 1]
        direcao = direcao / np.linalg.norm(direcao)

        # Vetores ortogonais à direção (plano normal)
        if np.allclose(direcao, [0, 0, 1]):
            orto1 = np.cross(direcao, [1, 0, 0])
        else:
            orto1 = np.cross(direcao, [0, 0, 1])
        orto1 = orto1 / np.linalg.norm(orto1)
        orto2 = np.cross(direcao, orto1)

        # Gera círculo ao redor do ponto da curva
        for j in range(resolucao_circular):
            ang = 2 * np.pi * j / resolucao_circular
            desloc = raio * (np.cos(ang) * orto1 + np.sin(ang) * orto2)
            vertice = ponto + desloc
            vertices.append(vertice.tolist())

    # Conecta os anéis de pontos com faces triangulares
    for i in range(resolucao_curva - 1):
        for j in range(resolucao_circular):
            i1 = i * resolucao_circular + j
            i2 = i * resolucao_circular + (j + 1) % resolucao_circular
            i3 = (i + 1) * resolucao_circular + j
            i4 = (i + 1) * resolucao_circular + (j + 1) % resolucao_circular

            # Dois triângulos por "quadrado"
            faces.append([vertices[i1], vertices[i3], vertices[i4]])
            faces.append([vertices[i1], vertices[i4], vertices[i2]])

    return vertices, faces