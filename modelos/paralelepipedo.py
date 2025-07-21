def modelar_paralelepipedo(base, altura, comprimento):
    """
    Modela um paralelepípedo (hiper retângulo) com base (x), altura (z) e comprimento (y).
    Retorna listas de vértices e faces triangulares.
    """
    vertices = []

    # Vértices inferiores (z = 0)
    vertices.append([0, 0, 0])                         # v0
    vertices.append([base, 0, 0])                      # v1
    vertices.append([base, comprimento, 0])            # v2
    vertices.append([0, comprimento, 0])               # v3

    # Vértices superiores (z = altura)
    vertices.append([0, 0, altura])                    # v4
    vertices.append([base, 0, altura])                 # v5
    vertices.append([base, comprimento, altura])       # v6
    vertices.append([0, comprimento, altura])          # v7

    # Define as 6 faces (2 triângulos por face)
    faces = [
        # Base inferior
        [vertices[0], vertices[1], vertices[2]],
        [vertices[0], vertices[2], vertices[3]],
        
        # Base superior
        [vertices[4], vertices[5], vertices[6]],
        [vertices[4], vertices[6], vertices[7]],
        
        # Frente
        [vertices[0], vertices[1], vertices[5]],
        [vertices[0], vertices[5], vertices[4]],
        
        # Trás
        [vertices[2], vertices[3], vertices[7]],
        [vertices[2], vertices[7], vertices[6]],
        
        # Direita
        [vertices[1], vertices[2], vertices[6]],
        [vertices[1], vertices[6], vertices[5]],
        
        # Esquerda
        [vertices[3], vertices[0], vertices[4]],
        [vertices[3], vertices[4], vertices[7]],
    ]

    return vertices, faces