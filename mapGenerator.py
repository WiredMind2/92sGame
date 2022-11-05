import base64
import time

from utils import Vector2
from enums import *
from perlin import Perlin2D

class MapGenerator:
    def __init__(self):
        pass

class Map:
    """
    Interface pour accéder aux données de la carte
    """

    def __init__(self, seed=None):
        self.seed = seed or time.time()

    def get_chunk(self, x, y):
        """
        Génère et renvoie les données d'un chunk 
        """

        data = {
            'x': x,
            'y': y,
            'links': [],
            'global_seed': self.seed
        }
        chunk = Chunk(**data)
        return chunk
    
class Chunk:
    """
    Contient les données d'un chunk (32*32 cells) de la map
    """

    def __init__(self, x, y, links, global_seed=None):
        self.x, self.y = x, y
        self.links = links
        self.global_seed = global_seed or 0

        self.generate()

    def generate(self):
        """
        Génère le chunk à partir de la seed et du context(links)
        """

        freq = 6 # = zoom
        noise_gen = Perlin2D(self.seed)

        data = []
        for x in range(32):
            data.append([])
            for y in range(32):
                cell = Cell()
                cell.x = self.x + x
                cell.y = self.y + y

                noise = noise_gen.noise(Vector2(x, y)/freq)/2 + 0.5 # [0, 1]

                # TODO - Join with closest chunk (use links data)

                if noise < 0.4:
                    cell.type = CellType.WATER
                elif noise < 0.55:
                    cell.type = CellType.GRASS
                else:
                    cell.type = CellType.MOUNTAIN
                
                cell.validate() # Check if all fields are correct

                data[x].append(cell)

        self.data = data
        return data
    
    def get(self, x, y):
        return self.data[x][y]

    @property
    def seed(self):
        seed = base64.b64encode(str((self.x, self.y, self.global_seed)).encode('utf-8'))
        return seed

    def array(self):
        """
        Renvoie les données sous forme de liste
        """

        return self.data

class Cell:
    """
    Contient les données d'une cellule
    """

    def __init__(self):
        self.args = [ # (name, type, allow_none)
            ('type', CellType, False),
            ('x', int, False),
            ('y', int, False)
        ]
        for name, type, allow_none in self.args:
            setattr(self, name, None)

    def validate(self):
        # Check if cell data is valid
        for name, type, allow_none in self.args:
            val = getattr(self, name)
            if not allow_none and val is None:
                raise ValueError(f"Cell.{name} cannot be None!")
            if not isinstance(val, type):
                raise TypeError(f"Cell.{name} should be of type {type}")

if __name__ == "__main__":
    map = Map('seed') # initialize map instance
    
    colors = {
        CellType.WATER: '\033[94m',
        CellType.MOUNTAIN: '\033[93m',
        CellType.GRASS: '\033[92m'
    }

    for m_y in range(6):
        out = ""
        chunk = map.get_chunk(0, m_y) # get chunk data

        # generate colors
        for x, row in enumerate(chunk.array()):
            for y, cell in enumerate(row):
                out += colors[cell.type] + str(cell.type.value)
            out += "\n"
        out = out[:-1] + '----\n'
        # show
        print(out, end="")