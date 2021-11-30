import copy

class move():
    def __init__(self, board, piece, origin, destination, eats = False):
        self.piece = piece
        self.origin = origin
        self.board = board
        self.destination = destination
        self.eats = eats
    def simulate(self):
        boardD = copy.deepcopy(self.board)
        boardD.layout[self.destination[1]][self.destination[0]] = self.piece
        boardD.layout[self.origin[1]][self.origin[0]] = None
        return boardD
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
        boardD = self.board
        boardD.layout[move.destination[1]][move.destination[0]] = move.piece
        boardD.layout[move.origin[1]][move.origin[0]] = None
    def legalMoves(self):
        moves = []
        case = (0, 0)
        for row in self.board.layout:
            for piec in row:
                if piec:
                    if piec.type == "rook" and piec.color == self.turn:
                        for i in range(1, 8):
                            if case[1]+i <= 7:
                                if self.board.layout[case[1]+i][case[0]] == None:
                                    moves.append(move(self.board, piec, case, (case[0], case[1]+i)))
                                else:
                                    if self.board.layout[case[1]+i][case[0]].color != piec.color:
                                        moves.append(move(self.board, piec, case, (case[0], case[1]+i), True))
                                    break
                            else:
                                break
                        for i in range(1, 8):
                            if case[1]-i >= 0:
                                if self.board.layout[case[1]-i][case[0]] == None:
                                    moves.append(move(self.board, piec, case, (case[0], case[1]-i)))
                                else:
                                    if self.board.layout[case[1]-i][case[0]].color != piec.color:
                                        moves.append(move(self.board, piec, case, (case[0], case[1]-i), True))
                                    break
                            else:
                                break
                        for i in range(1, 8):
                            if case[0]+i <= 7:
                                if self.board.layout[case[1]][case[0]+i] == None:
                                    moves.append(move(self.board, piec, case, (case[0]+i, case[1])))
                                else:
                                    if self.board.layout[case[1]][case[0]+i].color != piec.color:
                                        moves.append(move(self.board, piec, case, (case[0]+i, case[1]), True))
                                    break
                            else:
                                break
                        for i in range(1, 8):
                            if case[0]-i >= 0:
                                if self.board.layout[case[1]][case[0]-i] == None:
                                    moves.append(move(self.board, piec, case, (case[0]-i, case[1])))
                                else:
                                    if self.board.layout[case[1]][case[0]-i].color != piec.color:
                                        moves.append(move(self.board, piec, case, (case[0]-i, case[1]), True))
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
    def __init__(self, board = [[piece("rook", "white"), piece("knight", "white"), piece("bishop", "white"), piece("king", "white"), piece("queen", "white"), piece("bishop", "white"), piece("knight", "white"), piece("rook", "white")], [None, piece("pawn", "white"), piece("pawn", "white"), piece("pawn", "white"), piece("pawn", "white"), piece("pawn", "white"), piece("pawn", "white"), piece("pawn", "white")], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [piece("pawn", "black"), piece("pawn", "black"), piece("pawn", "black"), piece("pawn", "black"), piece("pawn", "black"), piece("pawn", "black"), piece("pawn", "black"), piece("pawn", "black")], [piece("rook", "black"), piece("knight", "black"), piece("bishop", "black"), piece("king", "black"), piece("queen", "black"), piece("bishop", "black"), piece("knight", "black"), piece("rook", "black")]]):
        self.layout = board
    def printBoard(self):
        for row in self.layout:
            for piec in row:
                if piec:
                    print(lettersName[piec.type][piec.color], end=";")
                else:
                    print(" ", end=";")
            print()

newBoard = board()
theGame = game(newBoard)
theGame.move(theGame.legalMoves()[0])
theGame.board.printBoard()