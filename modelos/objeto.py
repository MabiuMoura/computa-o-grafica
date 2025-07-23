import numpy as np
import math
from utils import curva_hermite

class Objeto3D:
    def __init__(self):
        self.vertices = None
        self.faces = None
        self.forma = None
        self.resolucao = None
        self.resolucao_circular = None
        self.resolucao_curva = None
    
    def atribuir_faces(self):
        self.faces = []

        if self.forma == "paralelepipedo":
            n_vertices = len(self.vertices)

            # Caso padrão com apenas 8 vértices
            if n_vertices == 8:
                self.faces = [
                    [0, 1, 2], [0, 2, 3],       # Base inferior
                    [4, 5, 6], [4, 6, 7],       # Base superior
                    [0, 1, 5], [0, 5, 4],       # Frente
                    [2, 3, 7], [2, 7, 6],       # Trás
                    [1, 2, 6], [1, 6, 5],       # Direita
                    [3, 0, 4], [3, 4, 7],       # Esquerda
                ]
            else:
                # Supondo que foi gerado com subdivisões regulares
                # Recupera a resolução (raiz cúbica do número de pontos aproximadamente)
                resolucao = round((n_vertices) ** (1 / 3)) - 1

                def idx(i, j, k):
                    return k * (resolucao + 1)**2 + j * (resolucao + 1) + i

                for k in range(resolucao + 1):
                    for j in range(resolucao):
                        for i in range(resolucao):
                            # base inferior (k=0)
                            if k == 0:
                                v0 = idx(i, j, k)
                                v1 = idx(i + 1, j, k)
                                v2 = idx(i + 1, j + 1, k)
                                v3 = idx(i, j + 1, k)
                                self.faces.append([v0, v1, v2])
                                self.faces.append([v0, v2, v3])
                            # base superior (k=res)
                            if k == resolucao:
                                v0 = idx(i, j, k)
                                v1 = idx(i + 1, j, k)
                                v2 = idx(i + 1, j + 1, k)
                                v3 = idx(i, j + 1, k)
                                self.faces.append([v0, v2, v1])
                                self.faces.append([v0, v3, v2])

                # faces laterais
                for k in range(resolucao):
                    for j in range(resolucao + 1):
                        for i in range(resolucao):
                            # lateral y=0 (frente)
                            if j == 0:
                                v0 = idx(i, j, k)
                                v1 = idx(i + 1, j, k)
                                v2 = idx(i + 1, j, k + 1)
                                v3 = idx(i, j, k + 1)
                                self.faces.append([v0, v1, v2])
                                self.faces.append([v0, v2, v3])
                            # lateral y=max (trás)
                            if j == resolucao:
                                v0 = idx(i, j, k)
                                v1 = idx(i + 1, j, k)
                                v2 = idx(i + 1, j, k + 1)
                                v3 = idx(i, j, k + 1)
                                self.faces.append([v0, v2, v1])
                                self.faces.append([v0, v3, v2])
                    for i in range(resolucao + 1):
                        for j in range(resolucao):
                            # lateral x=0 (esquerda)
                            if i == 0:
                                v0 = idx(i, j, k)
                                v1 = idx(i, j + 1, k)
                                v2 = idx(i, j + 1, k + 1)
                                v3 = idx(i, j, k + 1)
                                self.faces.append([v0, v1, v2])
                                self.faces.append([v0, v2, v3])
                            # lateral x=max (direita)
                            if i == resolucao:
                                v0 = idx(i, j, k)
                                v1 = idx(i, j + 1, k)
                                v2 = idx(i, j + 1, k + 1)
                                v3 = idx(i, j, k + 1)
                                self.faces.append([v0, v2, v1])
                                self.faces.append([v0, v3, v2])

        elif self.forma == "reta":
            self.faces = [[0, 1, 1]]  # apenas para visualização

        elif self.forma == "cilindro":
            for i in range(self.resolucao):
                i_base = i * 2
                i_topo = i_base + 1
                i_base_next = (i_base + 2) % (self.resolucao * 2)
                i_topo_next = (i_base_next + 1) % (self.resolucao * 2)

                self.faces.append([i_base, i_base_next, i_topo_next])
                self.faces.append([i_base, i_topo_next, i_topo])

                self.faces.append([self.base_center_index, i_base_next, i_base])
                self.faces.append([self.top_center_index, i_topo, i_topo_next])

        elif self.forma == "cano_reto":
            for i in range(self.resolucao):
                i1 = i * 4
                i2 = ((i + 1) % self.resolucao) * 4

                # Lateral externa
                self.faces.append([i1, i2, i2 + 1])
                self.faces.append([i1, i2 + 1, i1 + 1])

                # Lateral interna (invertida)
                self.faces.append([i1 + 2, i2 + 3, i2 + 2])
                self.faces.append([i1 + 2, i1 + 3, i2 + 3])

                # Tampa inferior
                self.faces.append([i1, i1 + 2, i2 + 2])
                self.faces.append([i1, i2 + 2, i2])

                # Tampa superior
                self.faces.append([i1 + 1, i2 + 1, i2 + 3])
                self.faces.append([i1 + 1, i2 + 3, i1 + 3])
                
        elif self.forma == "cano_curvado":
            rc = self.resolucao_circular
            rcv = self.resolucao_curva

            for i in range(rcv - 1):
                for j in range(rc):
                    # índice dos vértices externos
                    i_ext1 = i * rc * 2 + j * 2
                    i_ext2 = i * rc * 2 + ((j + 1) % rc) * 2
                    i_ext3 = (i + 1) * rc * 2 + j * 2
                    i_ext4 = (i + 1) * rc * 2 + ((j + 1) % rc) * 2

                    # índice dos vértices internos
                    i_int1 = i_ext1 + 1
                    i_int2 = i_ext2 + 1
                    i_int3 = i_ext3 + 1
                    i_int4 = i_ext4 + 1

                    # Faces externas
                    self.faces.append([i_ext1, i_ext3, i_ext4])
                    self.faces.append([i_ext1, i_ext4, i_ext2])

                    # Faces internas (invertidas)
                    self.faces.append([i_int4, i_int3, i_int1])
                    self.faces.append([i_int2, i_int4, i_int1])

                    # Faces laterais (ligando externo ao interno)
                    self.faces.append([i_ext1, i_int1, i_int3])
                    self.faces.append([i_ext1, i_int3, i_ext3])

                    self.faces.append([i_int4, i_int2, i_ext2])
                    self.faces.append([i_int4, i_ext2, i_ext4])
            
            
            
    def modelar_paralelepipedo(self, base, altura, comprimento, resolucao=1):
        """
        Modela um paralelepípedo subdividido com base (x), comprimento (y) e altura (z).
        O parâmetro 'resolucao' define quantas subdivisões por eixo (mínimo 1).
        """
        self.forma = "paralelepipedo"
        self.vertices = []
        self.faces = []

        # Cria grid 3D de pontos
        for k in range(resolucao + 1):  # eixo z (altura)
            z = (k / resolucao) * altura
            for j in range(resolucao + 1):  # eixo y (comprimento)
                y = (j / resolucao) * comprimento
                for i in range(resolucao + 1):  # eixo x (base)
                    x = (i / resolucao) * base
                    self.vertices.append([x, y, z])

        self.atribuir_faces()
        
        
    def modelar_linha(self, tamanho=4, direcao=np.array([1, 0, 0]), origem=np.array([0, 0, 0])):
        """
        Cria uma linha reta no espaço 3D a partir de uma origem, direção e tamanho.
        Retorna uma lista de dois vértices.
        
        Parâmetros:
        - tamanho: comprimento da linha
        - direcao: vetor direção (será normalizado)
        - origem: ponto de início da linha
        """
        self.forma = "reta"
        self.vertices = []
        self.faces = []
        
        direcao = direcao / np.linalg.norm(direcao)  # normaliza a direção
        ponto_final = origem + direcao * tamanho

        self.vertices = [origem.tolist(), ponto_final.tolist()] 
        self.atribuir_faces()

    def modelar_cilindro(self, raio, altura, resolucao=32):
        """
        Modela um cilindro com base no raio e altura.
        Retorna listas de vértices e self.faces triangulares.
        """
        self.forma = "cilindro"
        self.vertices = []
        self.faces = []
        self.resolucao = resolucao

        # Gera os pontos ao redor da base e topo
        for i in range(self.resolucao):
            theta = 2 * math.pi * i / self.resolucao
            cos_t = math.cos(theta)
            sin_t = math.sin(theta)

            x = raio * cos_t
            y = raio * sin_t

            self.vertices.append([x, y, 0])         # base
            self.vertices.append([x, y, altura])    # top
            
        # Adiciona vértices centrais para base e topo
        self.base_center_index = len(self.vertices)
        self.vertices.append([0, 0, 0])  # centro da base

        self.top_center_index = len(self.vertices)
        self.vertices.append([0, 0, altura])

        self.atribuir_faces()
        
    def modelar_cano_reto(self, raio_interno, raio_externo, altura, resolucao=32):
        self.resolucao = resolucao
        self.forma = "cano_reto"
        self.vertices = []
        self.faces = []
        
        for i in range(self.resolucao):
            theta = 2 * math.pi * i / self.resolucao
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

        
        self.atribuir_faces()
        
        
    def gerar_cano_curvado(self, P0, P1, T0, T1, raio_externo=0.2, raio_interno=0.15, resolucao_circular=16, resolucao_curva=100):
        self.resolucao_circular = resolucao_circular
        self.resolucao_curva = resolucao_curva
        self.forma = "cano_curvado"
        self.vertices = []
        self.faces = []

        curva = curva_hermite(P0, P1, T0, T1, self.resolucao_curva)

        for i in range(self.resolucao_curva):
            ponto = curva[i]

            # Tangente da curva
            if i < self.resolucao_curva - 1:
                direcao = curva[i + 1] - curva[i]
            else:
                direcao = curva[i] - curva[i - 1]
            direcao = direcao / np.linalg.norm(direcao)

            # Vetores ortogonais ao plano
            if np.allclose(direcao, [0, 0, 1]):
                orto1 = np.cross(direcao, [1, 0, 0])
            else:
                orto1 = np.cross(direcao, [0, 0, 1])
            orto1 = orto1 / np.linalg.norm(orto1)
            orto2 = np.cross(direcao, orto1)

            for j in range(resolucao_circular):
                ang = 2 * np.pi * j / resolucao_circular
                desloc_ext = raio_externo * (np.cos(ang) * orto1 + np.sin(ang) * orto2)
                desloc_int = raio_interno * (np.cos(ang) * orto1 + np.sin(ang) * orto2)

                self.vertices.append((ponto + desloc_ext).tolist())  # externo
                self.vertices.append((ponto + desloc_int).tolist())  # interno

        self.atribuir_faces()

        

    def aplicar_escala(self, sx, sy, sz):
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

        vertices_escalados = [matriz_escala @ np.array(v) for v in self.vertices]
        self.vertices = vertices_escalados
    
    def aplicar_translacao(self, deslocamento):
        deslocamento = np.array(deslocamento)
        self.vertices = [v + deslocamento for v in self.vertices]

    def aplicar_rotacao(self, eixo, angulo_graus):
        angulo_rad = np.radians(angulo_graus)
        if eixo == 'x':
            R = np.array([[1, 0, 0],
                          [0, np.cos(angulo_rad), -np.sin(angulo_rad)],
                          [0, np.sin(angulo_rad), np.cos(angulo_rad)]])
        elif eixo == 'y':
            R = np.array([[np.cos(angulo_rad), 0, np.sin(angulo_rad)],
                          [0, 1, 0],
                          [-np.sin(angulo_rad), 0, np.cos(angulo_rad)]])
        elif eixo == 'z':
            R = np.array([[np.cos(angulo_rad), -np.sin(angulo_rad), 0],
                          [np.sin(angulo_rad), np.cos(angulo_rad), 0],
                          [0, 0, 1]])
        
        self.vertices = [R @ v for v in self.vertices]
