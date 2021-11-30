class move():
    def __init__(self, board, piece, origin, destination):
        self.piece = piece
        self.origin = origin
        self.destination = destination
    def simulate(self):
        pass
    def isLegal(self):
        pass


lettersName = {
    "rook": {"white": "♖", "black": "♜"},
    "knight": {"white": "♘", "black": "♞"},
    "bishop": {"white": "♗", "black": "♝"},
    "king": {"white": "♔", "black": "♚"},
    "queen": {"white": "♕", "black": "♛"},
    "pawn": {"white": "♙", "black": "♟"}
}

class game():
    def __init__(self, board):
        self.board = board
        self.turn = "white"
        self.nTurn = 1
    def move(self, move):
        pass
    def printBoard(self):
        for row in self.board.layout:
            for piec in row:
                if piec:
                    print(lettersName[piec.type][piec.color], end=";")
                else:
                    print(" ", end=";")
            print()
    def legalMoves(self):
        moves = []
        case = (0, 0)
        for row in self.board.layout:
            for piec in row:
                if piec:
                    if piec.type == "rook":
                        for i in range(1, 8):
                            if case[1]+i <= 7:
                                if self.board.layout[case[1]+i][case[0]] == None:
                                    moves.append(move(self.board, piec, case, (case[0], case[1]+i)))
                                else:
                                    break
                            else:
                                break
                        for i in range(1, 8):
                            if case[1]-i >= 0:
                                if self.board.layout[case[1]-i][case[0]] == None:
                                    moves.append(move(self.board, piec, case, (case[0], case[1]-i)))
                                else:
                                    break
                            else:
                                break
                        for i in range(1, 8):
                            if case[0]+i <= 7:
                                if self.board.layout[case[1]][case[0]+i] == None:
                                    moves.append(move(self.board, piec, case, (case[0]+i, case[1])))
                                else:
                                    break
                            else:
                                break
                        for i in range(1, 8):
                            if case[0]-i >= 0:
                                if self.board.layout[case[1]][case[0]-i] == None:
                                    moves.append(move(self.board, piec, case, (case[0]-i, case[1])))
                                else:
                                    break
                            else:
                                break
                case = (case[0]+1, case[1])
            case = (0, case[1]+1)
        return moves
        
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
    def __init__(self, board = [[piece("rook", "white"), piece("knight", "white"), piece("bishop", "white"), piece("king", "white"), piece("queen", "white"), piece("bishop", "white"), piece("knight", "white"), piece("rook", "white")], [piece("pawn", "white"), piece("pawn", "white"), piece("pawn", "white"), piece("pawn", "white"), piece("pawn", "white"), piece("pawn", "white"), piece("pawn", "white"), piece("pawn", "white")], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [piece("pawn", "black"), piece("pawn", "black"), piece("pawn", "black"), piece("pawn", "black"), piece("pawn", "black"), piece("pawn", "black"), piece("pawn", "black"), piece("pawn", "black")], [piece("rook", "black"), piece("knight", "black"), piece("bishop", "black"), piece("king", "black"), piece("queen", "black"), piece("bishop", "black"), piece("knight", "black"), piece("rook", "black")]]):
        self.layout = board

newBoard = board()
theGame = game(newBoard)
print(theGame.legalMoves())
theGame.printBoard()