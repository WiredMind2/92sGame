"""
Pour les classes qui n'ont nul part d'autre où aller
"""

import math

class Vector:
    """
    Représente un tuple coordonnées de dimension n: (x, y, z, ...)
    """

    def __init__(self, dim, *coords):
        self.dim = dim
        self.coords = coords[:dim]
    
    def _map(self, func):
        # Interne - Renvoie un tuple de coordonnées après avoir map sur func(i, coord)
        return tuple(map(func, enumerate(self.coords)))

    def dim_check(self, vec, op):
        # Interne - Vérifie que self et vec soient comparables
        if not isinstance(vec, Vector) or vec.dim != self.dim:
            raise TypeError(f"unsupported operand type(s) for {op}: '{type(self)}' and '{type(vec)}'")

    def get_dim(self, dim):
        # Renvoie la valeur correspondant à la dimension dim
        return self.coords[dim]
    
    def __getitem__(self, dim):
        return self.coords[dim]

    def __setitem__(self, dim, val):
        self.coords[dim] = val

    def __add__(self, to):
        # vec1 + vec2 = (x1+x2, y1+y2)
        self.dim_check(to, '+')
        return Vector(self.dim, self._map(lambda i, c: c + to[i]))

    def __sub__(self, to):
        # vec1 - vec2 = (x1-x2, y1-y2)
        self.dim_check(to, '-')
        return self.__add__(-to) # Yup i'm lazy

    def __mul__(self, n):
        # vec1 * n = (x*n, y*n)
        return Vector2(self.dim, self._map(lambda i, c: c*n))

    def __truediv__(self, n):
        # vec1 / n = (x/n, y/n)
        return Vector(self.dim, self._map(lambda i, c: c/n))

    def __floordiv__(self, n):
        # vec1 // n = (x//n, y//n)
        return Vector(self.dim, self._map(lambda i, c: c//n))
    
    def __eq__(self, to):
        # vec1 == vec2
        self.dim_check(to, '==')
        return all(self._map(lambda i, c: c == to[i]))
    
    def __ne__(self, to):
        # vec1 != vec2
        self.dim_check(to, '!=')
        return not self.__eq__(to)
    
    def __lt__(self, to):
        # vec1 < vec2 <=> |vec1|^2 < |vec2|^2
        self.dim_check(to, '<')
        return self.sqr_norm() < to.sqr_norm()
    
    def __le__(self, to):
        # vec1 <= vec2
        self.dim_check(to, '<=')
        return self.__eq__(to) or self.__lt__(to)

    def __ge__(self, to):
        # vec1 >= vec2
        self.dim_check(to, '>=')
        return not self.__lt__(to)

    def __neg__(self):
        # -vec = (-x, -y)
        return Vector(self.dim, self._map(lambda i, c: -c))
    
    def __round__(self):
        # round(vec) = (round(x), round(y))
        return Vector(self.dim, self._map(lambda i, c: round(c)))

    def sqr_norm(self):
        # |vec|^2 => bcp plus rapide que norm() et permet toutes les comparaisons
        return sum(self._map(lambda i, c: c**2))

    def norm(self):
        # |vec| => slower 
        return math.sqrt(self.sqr_norm())
    
class Vector2 (Vector):
    """
    Représente un couple de coordonnées (x, y)
    """
    def __init__(self, *coords):
        super().__init__(2, *coords)

class Vector3 (Vector):
    """
    Représente un triplet de coordonnées (x, y, z)
    """
    def __init__(self, *coords):
        super().__init__(3, *coords)