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
    def legalMoves(self):
        pass
        
class piece():
    def __init__(self, type, color, alive = True):
        if not type in ["rook", "knight", "bishop", "king", "queen", "pawn"]:
            raise TypeError(type, "is not a valid piece type")
        if not color in ["white", "black"]:
            raise TypeError(color, "is not a valid chess color")
        self.type = type
        self.color = color
        self.alive = alive
    def legalMoves(self):
        pass
    
class board():
    def __init__(self, board = [[piece("rook", "white"), piece("knight", "white"), piece("bishop", "white"), piece("king", "white"), piece("queen", "white"), piece("bishop", "white"), piece("knight", "white"), piece("rook", "white")], [piece("pawn", "white"), piece("pawn", "white"), piece("pawn", "white"), piece("pawn", "white"), piece("pawn", "white"), piece("pawn", "white"), piece("pawn", "white"), piece("pawn", "white")], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [], []]):
        self.layout = board

newBoard = board()
theGame = game(newBoard)
print(len(theGame.board.layout))