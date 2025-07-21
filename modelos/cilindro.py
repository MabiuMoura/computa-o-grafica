import math

def modelar_cilindro(raio, altura, resolucao=32):
    """
    Modela um cilindro com base no raio e altura.
    Retorna listas de vértices e faces triangulares.
    """
    vertices = []
    faces = []

    # Gera os pontos ao redor da base e topo
    for i in range(resolucao):
        theta = 2 * math.pi * i / resolucao
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)

        x = raio * cos_t
        y = raio * sin_t

        vertices.append([x, y, 0])         # base
        vertices.append([x, y, altura])    # topo

    # Conecta laterais e tampas
    for i in range(resolucao):
        i_base = i * 2
        i_topo = i_base + 1
        i_base_next = (i_base + 2) % (resolucao * 2)
        i_topo_next = (i_base_next + 1) % (resolucao * 2)

        # Lateral
        faces.append([vertices[i_base], vertices[i_base_next], vertices[i_topo_next]])
        faces.append([vertices[i_base], vertices[i_topo_next], vertices[i_topo]])

        # Tampa inferior
        faces.append([[0, 0, 0], vertices[i_base_next], vertices[i_base]])

        # Tampa superior
        faces.append([[0, 0, altura], vertices[i_topo], vertices[i_topo_next]])

    return vertices, faces