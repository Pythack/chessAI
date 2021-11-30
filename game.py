class board():
    def __init__(self, isDefault = True):
        pass

class move():
    def __init__(self, board, piece, origin, destination):
        self.piece = piece
        self.origin = origin
        self.destination = destination
    def simulate(self):
        pass
    def isLegal(self):
        pass

class game():
    def __init__(self, board):
        self.board = board
    def move(self, move):
        pass
        
class piece():
    def __init__(self, type, color, game, alive = True):
        self.type = type
        self.color = color
        self.game = game
        self.alive = alive
    def legalMoves(self):
        pass