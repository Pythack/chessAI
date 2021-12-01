import copy

class move():
    def __init__(self, board, piece, origin, destination, eats = None):
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
    def isLegal(self, color):
        simulation = self.simulate()
        for i in simulation.legalMoves():
            if i.eats and i.piece.color != color:
                if i.eats.type == "king" and i.eats.color != i.piece.color:
                    return False
        return True


lettersName = {
    "rook": {"white": "♖", "black": "♜"},
    "knight": {"white": "♘", "black": "♞"},
    "bishop": {"white": "♗", "black": "♝"},
    "king": {"white": "♔", "black": "♚"},
    "queen": {"white": "♕", "black": "♛"},
    "pawn": {"white": "♙", "black": "♟"}
}

def checkColor(all, turn, piec):
    checkColor = piec.color == turn
    if all:
        checkColor = True
    return checkColor

class game():
    def __init__(self, board):
        self.board = board
        self.turn = "white"
        self.nTurn = 1
    def move(self, move):
        boardD = self.board
        boardD.layout[move.destination[1]][move.destination[0]] = move.piece
        boardD.layout[move.origin[1]][move.origin[0]] = None
        self.nTurn +=1
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"
        return True
    def legalMoves(self, all = False):
        moves = []
        case = (0, 0)
        for row in self.board.layout:
            for piec in row:
                if piec:
                    if piec.type == "rook" and checkColor(all, self.turn, piec):
                        for i in range(1, 8):
                            if case[1]+i <= 7:
                                if self.board.layout[case[1]+i][case[0]] == None:
                                    moves.append(move(self.board, piec, case, (case[0], case[1]+i)))
                                else:
                                    if self.board.layout[case[1]+i][case[0]].color != piec.color:
                                        moves.append(move(self.board, piec, case, (case[0], case[1]+i), self.board.layout[case[1]+i][case[0]]))
                                    break
                            else:
                                break
                        for i in range(1, 8):
                            if case[1]-i >= 0:
                                if self.board.layout[case[1]-i][case[0]] == None:
                                    moves.append(move(self.board, piec, case, (case[0], case[1]-i)))
                                else:
                                    if self.board.layout[case[1]-i][case[0]].color != piec.color:
                                        moves.append(move(self.board, piec, case, (case[0], case[1]-i), self.board.layout[case[1]-i][case[0]]))
                                    break
                            else:
                                break
                        for i in range(1, 8):
                            if case[0]+i <= 7:
                                if self.board.layout[case[1]][case[0]+i] == None:
                                    moves.append(move(self.board, piec, case, (case[0]+i, case[1])))
                                else:
                                    if self.board.layout[case[1]][case[0]+i].color != piec.color:
                                        moves.append(move(self.board, piec, case, (case[0]+i, case[1]), self.board.layout[case[1]][case[0]+i]))
                                    break
                            else:
                                break
                        for i in range(1, 8):
                            if case[0]-i >= 0:
                                if self.board.layout[case[1]][case[0]-i] == None:
                                    moves.append(move(self.board, piec, case, (case[0]-i, case[1])))
                                else:
                                    if self.board.layout[case[1]][case[0]-i].color != piec.color:
                                        moves.append(move(self.board, piec, case, (case[0]-i, case[1]), self.board.layout[case[1]][case[0]-i]))
                                    break
                            else:
                                break
                    if piec.type == "bishop" and checkColor(all, self.turn, piec):
                        for i in range(1, 8):
                            if case[1]+i <= 7 and case[0]+i <= 7:
                                if self.board.layout[case[1]+i][case[0]+i] == None:
                                    moves.append(move(self.board, piec, case, (case[0]+i, case[1]+i)))
                                else:
                                    if self.board.layout[case[1]+i][case[0]+i].color != piec.color:
                                        moves.append(move(self.board, piec, case, (case[0]+i, case[1]+i), self.board.layout[case[1]+i][case[0]+i]))
                                    break
                            else:
                                break
                        for i in range(1, 8):
                            if case[1]-i >= 0 and case[0]-i >= 0:
                                if self.board.layout[case[1]-i][case[0]-i] == None:
                                    moves.append(move(self.board, piec, case, (case[0]-i, case[1]-i)))
                                else:
                                    if self.board.layout[case[1]-i][case[0]-i].color != piec.color:
                                        moves.append(move(self.board, piec, case, (case[0]-i, case[1]-i), self.board.layout[case[1]-i][case[0]-i]))
                                    break
                            else:
                                break
                        for i in range(1, 8):
                            if case[0]+i <= 7 and case[1]-i >= 0:
                                if self.board.layout[case[1]-i][case[0]+i] == None:
                                    moves.append(move(self.board, piec, case, (case[0]+i, case[1]-i)))
                                else:
                                    if self.board.layout[case[1]-i][case[0]+i].color != piec.color:
                                        moves.append(move(self.board, piec, case, (case[0]+i, case[1]-i), self.board.layout[case[1]-i][case[0]+i]))
                                    break
                            else:
                                break
                        for i in range(1, 8):
                            if case[0]-i >= 0 and case[1]+i <= 7:
                                if self.board.layout[case[1]+i][case[0]-i] == None:
                                    moves.append(move(self.board, piec, case, (case[0]-i, case[1]+i)))
                                else:
                                    if self.board.layout[case[1]+i][case[0]-i].color != piec.color:
                                        moves.append(move(self.board, piec, case, (case[0]-i, case[1]+i), self.board.layout[case[1]+i][case[0]-i]))
                                    break
                            else:
                                break
                case = (case[0]+1, case[1])
            case = (0, case[1]+1)
        finalMoves = []
        for mov in moves:
            if mov.isLegal(mov.piece.color):
                finalMoves.append(mov)
        return finalMoves
        
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
    def __init__(self, board = [[piece("rook", "white"), piece("knight", "white"), None, piece("king", "white"), piece("queen", "white"), piece("bishop", "white"), piece("knight", "white"), piece("rook", "white")], [None, piece("pawn", "white"), piece("pawn", "white"), piece("bishop", "white"), piece("pawn", "white"), piece("pawn", "white"), piece("pawn", "white"), piece("pawn", "white")], [None, None, None, None, None, None, None, None], [None, None, None, piece("rook", "black"), None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [piece("pawn", "black"), piece("pawn", "black"), piece("pawn", "black"), piece("pawn", "black"), piece("pawn", "black"), piece("pawn", "black"), piece("pawn", "black"), piece("pawn", "black")], [piece("rook", "black"), piece("knight", "black"), piece("bishop", "black"), piece("king", "black"), piece("queen", "black"), piece("bishop", "black"), piece("knight", "black"), piece("rook", "black")]]):
        self.layout = board
    def printBoard(self):
        for row in self.layout:
            for piec in row:
                if piec:
                    print(lettersName[piec.type][piec.color], end=";")
                else:
                    print(" ", end=";")
            print()
    def legalMoves(self):
        moves = []
        case = (0, 0)
        for row in self.layout:
            for piec in row:
                if piec:
                    if piec.type == "rook":
                        for i in range(1, 8):
                            if case[1]+i <= 7:
                                if self.layout[case[1]+i][case[0]] == None:
                                    moves.append(move(self, piec, case, (case[0], case[1]+i)))
                                else:
                                    if self.layout[case[1]+i][case[0]].color != piec.color:
                                        moves.append(move(self, piec, case, (case[0], case[1]+i), self.layout[case[1]+i][case[0]]))
                                    break
                            else:
                                break
                        for i in range(1, 8):
                            if case[1]-i >= 0:
                                if self.layout[case[1]-i][case[0]] == None:
                                    moves.append(move(self, piec, case, (case[0], case[1]-i)))
                                else:
                                    if self.layout[case[1]-i][case[0]].color != piec.color:
                                        moves.append(move(self, piec, case, (case[0], case[1]-i), self.layout[case[1]-i][case[0]]))
                                    break
                            else:
                                break
                        for i in range(1, 8):
                            if case[0]+i <= 7:
                                if self.layout[case[1]][case[0]+i] == None:
                                    moves.append(move(self, piec, case, (case[0]+i, case[1])))
                                else:
                                    if self.layout[case[1]][case[0]+i].color != piec.color:
                                        moves.append(move(self, piec, case, (case[0]+i, case[1]), self.layout[case[1]][case[0]+i]))
                                    break
                            else:
                                break
                        for i in range(1, 8):
                            if case[0]-i >= 0:
                                if self.layout[case[1]][case[0]-i] == None:
                                    moves.append(move(self, piec, case, (case[0]-i, case[1])))
                                else:
                                    if self.layout[case[1]][case[0]-i].color != piec.color:
                                        moves.append(move(self, piec, case, (case[0]-i, case[1]), self.layout[case[1]][case[0]-i]))
                                    break
                            else:
                                break
                    if piec.type == "bishop":
                        for i in range(1, 8):
                            if case[1]+i <= 7 and case[0]+i <= 7:
                                if self.layout[case[1]+i][case[0]+i] == None:
                                    moves.append(move(self, piec, case, (case[0]+i, case[1]+i)))
                                else:
                                    if self.layout[case[1]+i][case[0]+i].color != piec.color:
                                        moves.append(move(self, piec, case, (case[0]+i, case[1]+i), self.layout[case[1]+i][case[0]+i]))
                                    break
                            else:
                                break
                        for i in range(1, 8):
                            if case[1]-i >= 0 and case[0]-i >= 0:
                                if self.layout[case[1]-i][case[0]-i] == None:
                                    moves.append(move(self, piec, case, (case[0]-i, case[1]-i)))
                                else:
                                    if self.layout[case[1]-i][case[0]-i].color != piec.color:
                                        moves.append(move(self, piec, case, (case[0]-i, case[1]-i), self.layout[case[1]-i][case[0]-i]))
                                    break
                            else:
                                break
                        for i in range(1, 8):
                            if case[0]+i <= 7 and case[1]-i >= 0:
                                if self.layout[case[1]-i][case[0]+i] == None:
                                    moves.append(move(self, piec, case, (case[0]+i, case[1]-i)))
                                else:
                                    if self.layout[case[1]-i][case[0]+i].color != piec.color:
                                        moves.append(move(self, piec, case, (case[0]+i, case[1]-i), self.layout[case[1]-i][case[0]+i]))
                                    break
                            else:
                                break
                        for i in range(1, 8):
                            if case[0]-i >= 0 and case[1]+i <= 7:
                                if self.layout[case[1]+i][case[0]-i] == None:
                                    moves.append(move(self, piec, case, (case[0]-i, case[1]+i)))
                                else:
                                    if self.layout[case[1]+i][case[0]-i].color != piec.color:
                                        moves.append(move(self, piec, case, (case[0]-i, case[1]+i), self.layout[case[1]+i][case[0]-i]))
                                    break
                            else:
                                break
                case = (case[0]+1, case[1])
            case = (0, case[1]+1)
        return moves


if __name__ == "__main__":
    newBoard = board()
    theGame = game(newBoard)
    while True:
        index0 = 0
        print("Available moves:")
        for i in theGame.legalMoves():
            print("---")
            print(index0)
            i.simulate().printBoard()
            index0 += 1
        print("The current board:")
        theGame.board.printBoard()
        index = int(input())
        theGame.move(theGame.legalMoves()[index])
    theGame.board.printBoard()