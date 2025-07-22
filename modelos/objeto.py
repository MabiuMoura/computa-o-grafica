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
            self.faces = [
                # Base inferior
                [self.vertices[0], self.vertices[1], self.vertices[2]],
                [self.vertices[0], self.vertices[2], self.vertices[3]],
                
                # Base superior
                [self.vertices[4], self.vertices[5], self.vertices[6]],
                [self.vertices[4], self.vertices[6], self.vertices[7]],
                
                # Frente
                [self.vertices[0], self.vertices[1], self.vertices[5]],
                [self.vertices[0], self.vertices[5], self.vertices[4]],
                
                # Trás
                [self.vertices[2], self.vertices[3], self.vertices[7]],
                [self.vertices[2], self.vertices[7], self.vertices[6]],
                
                # Direita
                [self.vertices[1], self.vertices[2], self.vertices[6]],
                [self.vertices[1], self.vertices[6], self.vertices[5]],
                
                # Esquerda
                [self.vertices[3], self.vertices[0], self.vertices[4]],
                [self.vertices[3], self.vertices[4], self.vertices[7]],
            ]

        elif self.forma == "reta":
            self.faces = [
                [self.vertices[0], self.vertices[1], self.vertices[1]]  
            ]

        elif self.forma == "cilindro":
            altura = self.vertices[1][2]  # altura do topo
            for i in range(self.resolucao):
                i_base = i * 2
                i_topo = i_base + 1
                i_base_next = (i_base + 2) % (self.resolucao * 2)
                i_topo_next = (i_base_next + 1) % (self.resolucao * 2)

                # Lateral
                self.faces.append([self.vertices[i_base], self.vertices[i_base_next], self.vertices[i_topo_next]])
                self.faces.append([self.vertices[i_base], self.vertices[i_topo_next], self.vertices[i_topo]])

                # Tampa inferior (base)
                self.faces.append([self.vertices[self.base_center_index],
                                   self.vertices[i_base_next],
                                   self.vertices[i_base]])

                # Tampa superior (topo)
                self.faces.append([self.vertices[self.top_center_index],
                                   self.vertices[i_topo],
                                   self.vertices[i_topo_next]])

        elif self.forma == "cano_reto":
            for i in range(self.resolucao):
                i1 = i * 4
                i2 = ((i + 1) % self.resolucao) * 4

                # Lateral externa
                self.faces.append([self.vertices[i1], self.vertices[i2], self.vertices[i2 + 1]])
                self.faces.append([self.vertices[i1], self.vertices[i2 + 1], self.vertices[i1 + 1]])

                # Lateral interna (invertida)
                self.faces.append([self.vertices[i1 + 2], self.vertices[i2 + 3], self.vertices[i2 + 2]])
                self.faces.append([self.vertices[i1 + 2], self.vertices[i1 + 3], self.vertices[i2 + 3]])

                # Tampa inferior
                self.faces.append([self.vertices[i1], self.vertices[i1 + 2], self.vertices[i2 + 2]])
                self.faces.append([self.vertices[i1], self.vertices[i2 + 2], self.vertices[i2]])

                # Tampa superior
                self.faces.append([self.vertices[i1 + 1], self.vertices[i2 + 1], self.vertices[i2 + 3]])
                self.faces.append([self.vertices[i1 + 1], self.vertices[i2 + 3], self.vertices[i1 + 3]])

        elif self.forma == "cano_curvado":
            for i in range(self.resolucao_curva - 1):
                for j in range(self.resolucao_circular):
                    i1 = i * self.resolucao_circular + j
                    i2 = i * self.resolucao_circular + (j + 1) % self.resolucao_circular
                    i3 = (i + 1) * self.resolucao_circular + j
                    i4 = (i + 1) * self.resolucao_circular + (j + 1) % self.resolucao_circular

                    self.faces.append([self.vertices[i1], self.vertices[i3], self.vertices[i4]])
                    self.faces.append([self.vertices[i1], self.vertices[i4], self.vertices[i2]])    
        
        
        
    def modelar_paralelepipedo(self, base, altura, comprimento):
        """
        Modela um paralelepípedo (hiper retângulo) com base (x), altura (z) e comprimento (y).
        Retorna listas de vértices e faces triangulares.
        """
        self.forma = "paralelepipedo"
        self.vertices = []
        self.faces = []
        
        # Vértices inferiores (z = 0)
        self.vertices.append([0, 0, 0])                         # v0
        self.vertices.append([base, 0, 0])                      # v1
        self.vertices.append([base, comprimento, 0])            # v2
        self.vertices.append([0, comprimento, 0])               # v3

        # Vértices superiores (z = altura)
        self.vertices.append([0, 0, altura])                    # v4
        self.vertices.append([base, 0, altura])                 # v5
        self.vertices.append([base, comprimento, altura])       # v6
        self.vertices.append([0, comprimento, altura])          # v7

        # Define as 6 faces (2 triângulos por face)
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

        for i in range(self.resolucao):
            i1 = i * 4
            i2 = ((i + 1) % self.resolucao) * 4

            # Lateral externa
            self.faces.append([self.vertices[i1], self.vertices[i2], self.vertices[i2 + 1]])
            self.faces.append([self.vertices[i1], self.vertices[i2 + 1], self.vertices[i1 + 1]])

            # Lateral interna (invertida)
            self.faces.append([self.vertices[i1 + 2], self.vertices[i2 + 3], self.vertices[i2 + 2]])
            self.faces.append([self.vertices[i1 + 2], self.vertices[i1 + 3], self.vertices[i2 + 3]])

            # Tampa inferior
            self.faces.append([self.vertices[i1], self.vertices[i1 + 2], self.vertices[i2 + 2]])
            self.faces.append([self.vertices[i1], self.vertices[i2 + 2], self.vertices[i2]])

            # Tampa superior
            self.faces.append([self.vertices[i1 + 1], self.vertices[i2 + 1], self.vertices[i2 + 3]])
            self.faces.append([self.vertices[i1 + 1], self.vertices[i2 + 3], self.vertices[i1 + 3]])
        self.atribuir_faces()
        
        
    def gerar_cano_curvado(self, P0, P1, T0, T1, raio=0.2, resolucao_circular=16, resolucao_curva=100):
        self.resolucao_circular = resolucao_circular
        self.resolucao_curva = resolucao_curva
        self.forma = "cano_curvado"
        self.vertices = []
        self.faces = []
        
        curva = curva_hermite(P0, P1, T0, T1, self.resolucao_curva)

        for i in range(self.resolucao_curva):
            ponto = curva[i]

            # Aproximação da tangente para plano local
            if i < self.resolucao_curva - 1:
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
            for j in range(self.resolucao_circular):
                ang = 2 * np.pi * j / self.resolucao_circular
                desloc = raio * (np.cos(ang) * orto1 + np.sin(ang) * orto2)
                vertice = ponto + desloc
                self.vertices.append(vertice.tolist())

        # Conecta os anéis de pontos com self.faces triangulares
        for i in range(self.resolucao_curva - 1):
            for j in range(self.resolucao_circular):
                i1 = i * self.resolucao_circular + j
                i2 = i * self.resolucao_circular + (j + 1) % self.resolucao_circular
                i3 = (i + 1) * self.resolucao_circular + j
                i4 = (i + 1) * self.resolucao_circular + (j + 1) % self.resolucao_circular

                # Dois triângulos por "quadrado"
                self.faces.append([self.vertices[i1], self.vertices[i3], self.vertices[i4]])
                self.faces.append([self.vertices[i1], self.vertices[i4], self.vertices[i2]])
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
