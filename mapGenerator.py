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