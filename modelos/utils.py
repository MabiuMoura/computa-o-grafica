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


def aplicar_escala(vertices, sx, sy, sz):
    """
    Aplica escala nos vértices de um objeto 3D.
    
    Parâmetros:
    - vertices: lista de vértices [[x, y, z], ...]
    - sx, sy, sz: fatores de escala nos eixos X, Y e Z
    """
    matriz_escala = np.array([
        [sx,  0,  0],
        [0,  sy,  0],
        [0,   0, sz]
    ])

    vertices_escalados = [matriz_escala @ np.array(v) for v in vertices]
    return vertices_escalados

def aplicar_translacao(vertices, indice_vertice, destino):
    """
    Translada todos os vértices de um objeto 3D para que
    o vértice de índice `indice_vertice` vá para a posição `destino`.

    Parâmetros:
    - vertices: lista de vértices [[x, y, z], ...]
    - indice_vertice: índice do vértice de referência a ser movido
    - destino: coordenadas [dx, dy, dz] para onde o vértice deve ir
    """
    origem = np.array(vertices[indice_vertice])
    destino = np.array(destino)
    deslocamento = destino - origem

    vertices_transladados = [np.array(v) + deslocamento for v in vertices]
    return vertices_transladados


def aplicar_rotacao(vertices, eixo, angulo_graus):
    """
    Rotaciona os vértices de um objeto 3D em torno do eixo especificado.

    Parâmetros:
    - vertices: lista de vértices [[x, y, z], ...]
    - eixo: 'x', 'y' ou 'z'
    - angulo_graus: ângulo de rotação em graus
    """
    ang = np.radians(angulo_graus)

    if eixo == 'x':
        matriz_rot = np.array([
            [1, 0, 0],
            [0, np.cos(ang), -np.sin(ang)],
            [0, np.sin(ang),  np.cos(ang)]
        ])
    elif eixo == 'y':
        matriz_rot = np.array([
            [np.cos(ang), 0, np.sin(ang)],
            [0, 1, 0],
            [-np.sin(ang), 0, np.cos(ang)]
        ])
    elif eixo == 'z':
        matriz_rot = np.array([
            [np.cos(ang), -np.sin(ang), 0],
            [np.sin(ang),  np.cos(ang), 0],
            [0, 0, 1]
        ])
    else:
        raise ValueError("Eixo inválido. Use 'x', 'y' ou 'z'.")

    vertices_rotacionados = [matriz_rot @ np.array(v) for v in vertices]
    return vertices_rotacionados


def normalizar_solido(vertices, destino=[0, 0, 0], limite=10):
    """
    Normaliza os vértices de um sólido para que caibam dentro de um espaço de tamanho máximo 'limite'.
    Depois, translada o sólido para a posição 'destino'.

    Parâmetros:
    - vertices: lista de vértices [[x, y, z], ...]
    - destino: ponto para o qual o centro do objeto deve ser transladado
    - limite: valor máximo permitido em qualquer coordenada (default = 10)

    Retorna:
    - lista de vértices transformados
    """
    v = np.array(vertices)

    # 1. Centralizar o objeto na origem
    centro = np.mean(v, axis=0)
    centralizado = v - centro

    # 2. Calcular o maior valor absoluto das coordenadas
    max_coord = np.max(np.abs(centralizado))

    # 3. Calcular escala para caber no espaço [-limite/2, limite/2]
    fator_escala = (limite / 2.0) / max_coord if max_coord != 0 else 1
    escalado = centralizado * fator_escala

    # 4. Transladar para o destino
    destino = np.array(destino)
    final = escalado + destino

    return final.tolist()

def faces_para_indices(faces_em_vertices, lista_vertices_transformados, tolerancia=1e-6):
    """
    Converte faces definidas por vértices em faces por índices,
    comparando com a lista de vértices transformados usando np.allclose.

    faces_em_vertices: List[List[List[float]]]
    lista_vertices_transformados: List[List[float]]
    """
    faces_com_indices = []

    lista_vertices_np = [np.array(v) for v in lista_vertices_transformados]

    for face in faces_em_vertices:
        indices = []
        for vertice in face:
            vertice = np.array(vertice)
            encontrado = False
            for i, v_ref in enumerate(lista_vertices_np):
                if np.allclose(vertice, v_ref, atol=tolerancia):
                    indices.append(i)
                    encontrado = True
                    break
            if not encontrado:
                raise ValueError(f"Vértice {vertice.tolist()} não encontrado na lista transformada.")
        faces_com_indices.append(indices)

    return faces_com_indices