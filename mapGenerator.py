import math
import random

from utils import Vector2

class MapGenerator:
    def __init__(self):
        pass

class Map:
    """
    Interface pour accéder aux données de la carte
    """

    def __init__(self):
        pass

    def get_chunk(self, x, y):
        """
        Génère et renvoie les données d'un chunk 
        """

        chunk = Chunk()
        return chunk
    
class Chunk:
    """
    Contient les données d'un chunk de la map
    """

    def __init__(self):
        self.data = []

    def generate(self, seed, context):
        """
        Génère le chunk à partir de la seed et du context
        """

        data = ...

        return data
    
    def as_array(self):
        """
        Renvoie les données sous forme de liste
        """

        return self.data

class Perlin:
    """
    Perlin Noise Generator => génération d'un array de valeurs aléatoires cohérentes
    """
    def __init__(self) :
        self.perm1D = [2*random.random()-1 for _ in range(256)]
        self.perm2D = [[(2*random.random()-1,2*random.random()-1) for x in range(256)] for y in range(256)]

        self.fractal_factors = [(300, 1), (150, 2), (75, 4), (37.5, 8)]

    def noise1D(self, p):
        p0 = math.floor(p)
        p1 = p0 + 1

        t = p - p0
        fade_t = self.fade(t)

        g0 = self.grad1D(p0)
        g1 = self.grad1D(p1)

        return (1-fade_t)*g0*(p - p0) + fade_t*g1*(p - p1)

    def fractalNoise1D(self, p, factors=5):
        return sum(self.noise1D(p / i**2) / i**2 for i in range(1, factors+1))

    def fade(self, t):
        # t^3(t(t*6-15)+10)
        return t*t*t*(t*(t*6 - 15) + 10)

    def grad1D(self, p):
        return self.perm1D[p & 256-1]

    def noise2D(self, p):
        p0 = math.floor(p)
        p1 = p0 + (1, 0)
        p2 = p0 + (0, 1)
        p3 = p0 + (1, 1)

        g0 = self.grad2D(p0)
        g1 = self.grad2D(p1)
        g2 = self.grad2D(p2)
        g3 = self.grad2D(p3)

        t0 = p.x - p0.x
        fade_t0 = self.fade(t0)

        t1 = p.y - p0.y
        fade_t1 = self.fade(t1)

        p0p1 = (1 - fade_t0) * (g0 @ (p - p0)) + fade_t0 * (g1 @ (p - p1))
        p2p3 = (1 - fade_t0) * (g2 @ (p - p2)) + fade_t0 * (g3 @ (p - p3))

        return (1 - fade_t1) * p0p1 + fade_t1 * p2p3

    def fractalNoise2D(self, p, factors=5):
        return sum(self.noise2D(p / i**2) / i**2 for i in range(1, factors+1))
    
    def grad2D(self, p):
        return Vector2(*self.perm2D[p.x & 256-1][p.y & 256-1])


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import time

    p = Perlin()

    size = 50
    freq = 10

    # x = [i for i in range(size)]
    # y = [2*p.noise1D(i/freq) for i in range(size)]

    # plt.plot(x, y)

    # fractaly = [2*p.fractalNoise1D(i, 5)*3 for i in range(size)]

    # plt.plot(x, fractaly)

    zoom = 1/8

    noise = [[p.noise2D(Vector2(x, y)/freq/zoom) for x in range(size)] for y in range(size)]

    plt.figure()
    plt.imshow(noise, cmap='gray', interpolation='lanczos')


    # fractalnoise = [[p.fractalNoise2D(Vector2(x, y)) for x in range(size)] for y in range(size)]

    # plt.figure()
    # plt.imshow(fractalnoise, cmap='gray', interpolation='lanczos')

    plt.show()