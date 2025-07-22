import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

def plotar_malha_3d(vertices, faces, titulo="Objeto 3D", cor="orange", borda="black", alpha=0.9, linewidth=0.3,
                    ponto_destaque=None, eixos=None, vetor_olhar=None):
    """
    Plota uma malha 3D com destaques opcionais.

    - ponto_destaque: ponto especial para marcar (ex: origem do mundo).
    - eixos: dicionário com vetores u, v, w.
    - vetor_olhar: tupla (origem, destino) para desenhar vetor de olhar da câmera.
    """
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    mesh = Poly3DCollection(faces, facecolor=cor, edgecolor=borda, linewidths=linewidth, alpha=alpha)
    ax.add_collection3d(mesh)

    x_vals = [v[0] for v in vertices]
    y_vals = [v[1] for v in vertices]
    z_vals = [v[2] for v in vertices]

    margem = 0.5
    ax.set_xlim([min(x_vals) - margem, max(x_vals) + margem])
    ax.set_ylim([min(y_vals) - margem, max(y_vals) + margem])
    ax.set_zlim([min(z_vals) - margem, max(z_vals) + margem])

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title(titulo)

    if ponto_destaque:
        ax.scatter(*ponto_destaque, color='red', s=50)
        ax.text(*ponto_destaque, "Origem do Mundo", color='red')

    if eixos:
        origem = [0, 0, 0]
        u, v, w = eixos['u'], eixos['v'], eixos['w']
        ax.quiver(*origem, *u, length=1.0, color='blue', normalize=True)
        ax.text(*u, "u", color='blue')
        ax.quiver(*origem, *v, length=1.0, color='green', normalize=True)
        ax.text(*v, "v", color='green')
        ax.quiver(*origem, *w, length=1.0, color='red', normalize=True)
        ax.text(*w, "w", color='red')

    # Desenhar vetor de olhar da câmera
    if vetor_olhar:
        origem, destino = vetor_olhar
        direcao = np.array(destino) - np.array(origem)
        ax.quiver(*origem, *direcao, length=1.0, color='purple', normalize=True)
        ax.text(*destino, "Olhar", color='purple')

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



def normalizar_cena(vertices, limite=10.0, modo='uniforme'):
    """
    Normaliza os vértices para que caibam no intervalo [-limite, limite].
    
    Parâmetros:
    - vertices: lista de vértices [x, y, z]
    - limite: valor máximo em cada eixo
    - modo: 'uniforme' (mesmo fator para todos) ou 'por_eixo' (distorce para caber)
    """
    verts_np = np.array(vertices)
    if modo == 'uniforme':
        max_val = np.max(np.abs(verts_np))
        if max_val > limite:
            fator = limite / max_val
            print(f"[INFO] Normalizando cena (uniforme) com fator {fator:.3f}")
            return (verts_np * fator).tolist()
        return vertices
    elif modo == 'por_eixo':
        max_vals = np.max(np.abs(verts_np), axis=0)
        fatores = np.where(max_vals != 0, limite / max_vals, 1.0)
        print(f"[INFO] Normalizando cena (por eixo) com fatores: x={fatores[0]:.3f}, y={fatores[1]:.3f}, z={fatores[2]:.3f}")
        return (verts_np * fatores).tolist()


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


def projetar_perspectiva(vertices, d=5.0):
    """
    Aplica projeção perspectiva nos vértices.
    """
    vertices_proj = []
    for x, y, z in vertices:
        denom = z + d if z + d != 0 else 1e-5  # evita divisão por zero
        x_proj = (x * d) / denom
        y_proj = (y * d) / denom
        vertices_proj.append([x_proj, y_proj])
    return vertices_proj


def desenhar_em_2d(lista_vertices, lista_faces, cores):
    """
    Recebe listas de vértices e faces por objeto e plota em 2D.
    Cada objeto recebe uma cor da lista cores.
    """
    fig, ax = plt.subplots(figsize=(8, 8))

    for i, (verts, faces) in enumerate(zip(lista_vertices, lista_faces)):
        cor = cores[i % len(cores)]
        proj_verts = projetar_perspectiva(verts)

        for face in faces:
            pts = []
            for v in face:
                for j, original in enumerate(verts):
                    if np.allclose(original, v):
                        pts.append(proj_verts[j])
                        break
            if len(pts) >= 2:
                pts.append(pts[0])  # fechar o polígono
                xs, ys = zip(*pts)
                ax.plot(xs, ys, color=cor, linewidth=1)

    ax.set_aspect('equal')
    ax.set_title("Projeção Perspectiva 2D dos Sólidos")
    plt.grid(True)
    plt.show()