import numpy as np

def modelar_linha(tamanho=4, direcao=np.array([1, 0, 0]), origem=np.array([0, 0, 0])):
    """
    Cria uma linha reta no espaço 3D a partir de uma origem, direção e tamanho.
    Retorna uma lista de dois vértices.
    
    Parâmetros:
    - tamanho: comprimento da linha
    - direcao: vetor direção (será normalizado)
    - origem: ponto de início da linha
    """
    direcao = direcao / np.linalg.norm(direcao)  # normaliza a direção
    ponto_final = origem + direcao * tamanho

    self.vertices = [origem.tolist(), ponto_final.tolist()]
    return self.vertices