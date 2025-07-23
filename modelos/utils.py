import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

def plotar_malha_3d(vertices, faces, titulo="Objeto 3D", cor="orange", borda="black", alpha=0.9, linewidth=0.3):
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    triangulos = [[vertices[i] for i in face] for face in faces]  # espera listas puras
    mesh = Poly3DCollection(triangulos, facecolor=cor, edgecolor=borda, linewidths=linewidth, alpha=alpha)
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

    plt.tight_layout()
    plt.show()


def plotar_malhas_3d_multiplos(objetos, titulo="Cena 3D"):
    """
    Plota múltiplas malhas 3D em uma única figura.
    
    Parâmetro:
    - objetos: lista de tuplas no formato (vertices, faces, cor, nome)
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    for vertices, faces, cor, nome in objetos:
        mesh = Poly3DCollection([ [vertices[int(i)] for i in face] for face in faces ],
                                facecolor=cor, edgecolor="black", linewidths=0.3, alpha=0.9, label=nome)
        ax.add_collection3d(mesh)

    # Coletar todos os pontos para ajuste automático de eixos
    todos_vertices = np.concatenate([np.array(v) for v, _, _, _ in objetos])
    x_vals = todos_vertices[:, 0]
    y_vals = todos_vertices[:, 1]
    z_vals = todos_vertices[:, 2]

    margem = 0.5
    ax.set_xlim([x_vals.min() - margem, x_vals.max() + margem])
    ax.set_ylim([y_vals.min() - margem, y_vals.max() + margem])
    ax.set_zlim([z_vals.min() - margem, z_vals.max() + margem])

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
