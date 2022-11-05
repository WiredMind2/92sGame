import math
import random

from utils import Vector2


class Perlin1D:
    """
    Perlin Noise Generator => génération d'un array de valeurs aléatoires cohérentes
    """
    def __init__(self, seed) :
        gen = random.Random(seed or time.time())
        self.perm1D = [2*gen.random()-1 for _ in range(256)]

    def noise(self, p):
        p0 = math.floor(p)
        p1 = p0 + 1

        t = p - p0
        fade_t = self.fade(t)

        g0 = self.grad(p0)
        g1 = self.grad(p1)

        return (1-fade_t)*g0*(p - p0) + fade_t*g1*(p - p1)

    def fractalNoise(self, p, factors=5):
        return sum(self.noise(p / i**2) / i**2 for i in range(1, factors+1))

    def fade(self, t):
        # t^3(t(t*6-15)+10)
        return t*t*t*(t*(t*6 - 15) + 10)

    def grad(self, p):
        return self.perm1D[p & 256-1]

class Perlin2D:
    def __init__(self, seed=None) :
        gen = random.Random(seed or time.time())
        self.perm2D = [[(2*gen.random()-1,2*gen.random()-1) for x in range(256)] for y in range(256)]

    def noise(self, p):
        p0 = math.floor(p)
        p1 = p0 + (1, 0)
        p2 = p0 + (0, 1)
        p3 = p0 + (1, 1)

        g0 = self.grad(p0)
        g1 = self.grad(p1)
        g2 = self.grad(p2)
        g3 = self.grad(p3)

        t0 = p.x - p0.x
        fade_t0 = self.fade(t0)

        t1 = p.y - p0.y
        fade_t1 = self.fade(t1)

        p0p1 = (1 - fade_t0) * (g0 @ (p - p0)) + fade_t0 * (g1 @ (p - p1))
        p2p3 = (1 - fade_t0) * (g2 @ (p - p2)) + fade_t0 * (g3 @ (p - p3))

        return (1 - fade_t1) * p0p1 + fade_t1 * p2p3

    def fractalNoise(self, p, factors=5):
        return sum(self.noise(p / i**2) / i**2 for i in range(1, factors+1))
    
    def fade(self, t):
        # t^3(t(t*6-15)+10)
        return t*t*t*(t*(t*6 - 15) + 10)

    def grad(self, p):
        return Vector2(*self.perm2D[p.x & 256-1][p.y & 256-1])


if __name__ == "__main__":
    import time

    import matplotlib.pyplot as plt

    p1d = Perlin1D("fth")

    size = 200
    freq = 10

    # x = [i for i in range(size)]
    # y = [2*p1d.noise(i/freq) for i in range(size)]

    # plt.plot(x, y)

    # fractaly = [2*p1d.fractalNoise(i, 5)*3 for i in range(size)]

    # plt.plot(x, fractaly)

    p2d = Perlin2D()

    zoom = 1/8

    noise = [[p2d.noise(Vector2(x, y)/0.3) for x in range(size)] for y in range(size)]

    val_up = max((max(row) for row in noise))
    val_down = min((min(row) for row in noise))
    print(val_up, val_down)

    plt.figure()
    plt.imshow(noise, cmap='gray', interpolation='lanczos')


    # fractalnoise = [[p2d.fractalNoise(Vector2(x, y)) for x in range(size)] for y in range(size)]

    # plt.figure()
    # plt.imshow(fractalnoise, cmap='gray', interpolation='lanczos')

    plt.show()