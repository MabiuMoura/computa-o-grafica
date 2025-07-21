import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

def plotar_malha_3d(vertices, faces, titulo="Objeto 3D", cor="orange", borda="black", alpha=0.9, linewidth=0.3):
    """
    Plota uma malha 3D composta por vértices e faces triangulares.

    Parâmetros:
    - vertices: lista de vértices [x, y, z]
    - faces: lista de triângulos [[v1, v2, v3], ...]
    - titulo: título do gráfico
    - cor: cor da face
    - borda: cor da borda (edge)
    - alpha: transparência da malha
    - linewidth: espessura da linha da borda
    """
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Malha como coleção de polígonos
    mesh = Poly3DCollection(faces, facecolor=cor, edgecolor=borda, linewidths=linewidth, alpha=alpha)
    ax.add_collection3d(mesh)

    # Limites automáticos com margens
    x_vals = [v[0] for v in vertices]
    y_vals = [v[1] for v in vertices]
    z_vals = [v[2] for v in vertices]

    margem = 0.2
    ax.set_xlim([min(x_vals) - margem, max(x_vals) + margem])
    ax.set_ylim([min(y_vals) - margem, max(y_vals) + margem])
    ax.set_zlim([min(z_vals) - margem, max(z_vals) + margem])

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title(titulo)

    plt.tight_layout()
    plt.show()
    
    
def curva_hermite(P0, P1, T0, T1, n=100):
    """Gera pontos em uma curva de Hermite cúbica"""
    t = np.linspace(0, 1, n)[:, None]  # vetor coluna (n,1)

    h00 = 2*t**3 - 3*t**2 + 1
    h10 = t**3 - 2*t**2 + t
    h01 = -2*t**3 + 3*t**2
    h11 = t**3 - t**2

    H = h00 * P0 + h10 * T0 + h01 * P1 + h11 * T1
    return H

def transformar_vertices(vertices, escala=1.0, rotacao=np.eye(3), translacao=np.zeros(3)):
    """
    Aplica transformações (escala, rotação e translação) a uma lista de vértices.
    - vertices: lista de [x, y, z]
    - escala: escalar ou vetor 3D
    - rotacao: matriz 3x3
    - translacao: vetor 3D
    """
    novos_vertices = []
    for v in vertices:
        v = np.array(v)
        v = v * escala
        v = rotacao @ v
        v = v + translacao
        novos_vertices.append(v.tolist())
    return novos_vertices


def normalizar_cena(vertices, limite=10.0):
    """
    Garante que todos os vértices da cena estejam dentro do cubo [-limite, limite] em qualquer eixo.
    
    Parâmetros:
    - vertices: lista de vértices [x, y, z]
    - limite: valor máximo permitido para qualquer coordenada (padrão: 10.0)
    
    Retorna:
    - Lista de vértices normalizados (escalados para caber no limite)
    """
    max_val = np.max(np.abs(vertices))  # maior valor absoluto em qualquer eixo
    if max_val > limite:
        fator = limite / max_val
        print(f"[INFO] Normalizando cena com fator {fator:.3f}")
        return [ (np.array(v) * fator).tolist() for v in vertices ]
    return vertices  # já está dentro do limite