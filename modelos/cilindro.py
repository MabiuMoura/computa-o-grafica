import math

def modelar_cilindro(self, raio, altura, resolucao=32):
    """
    Modela um cilindro com base no raio e altura.
    Retorna listas de vértices e self.faces triangulares.
    """
    self.vertices = []
    self.faces = []

    # Gera os pontos ao redor da base e topo
    for i in range(resolucao):
        theta = 2 * math.pi * i / resolucao
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)

        x = raio * cos_t
        y = raio * sin_t

        self.vertices.append([x, y, 0])         # base
        self.vertices.append([x, y, altura])    # topo

    # Conecta laterais e tampas
    for i in range(resolucao):
        i_base = i * 2
        i_topo = i_base + 1
        i_base_next = (i_base + 2) % (resolucao * 2)
        i_topo_next = (i_base_next + 1) % (resolucao * 2)

        # Lateral
        self.faces.append([self.vertices[i_base], self.vertices[i_base_next], self.vertices[i_topo_next]])
        self.faces.append([self.vertices[i_base], self.vertices[i_topo_next], self.vertices[i_topo]])

        # Tampa inferior
        self.faces.append([[0, 0, 0], self.vertices[i_base_next], self.vertices[i_base]])

        # Tampa superior
        self.faces.append([[0, 0, altura], self.vertices[i_topo], self.vertices[i_topo_next]])

    return self.vertices, self.faces