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
    def toStr(self, sep = ""):
        xToChar = {
            0: "A",
            1: "B",
            2: "C",
            3: "D",
            4: "E",
            5: "F",
            6: "G",
            7: "H"
        }
        yToChar = [0, "7", "6", "5", "4", "3", "2", "1", "0"]
        oc = xToChar[self.origin[0]] + str(yToChar[int(self.origin[1])])
        dc = xToChar[self.destination[0]] + str(yToChar[int(self.destination[1])])
        return oc + sep + dc


lettersName = {
    "rook": {"black": "♖", "white": "♜"},
    "knight": {"black": "♘", "white": "♞"},
    "bishop": {"black": "♗", "white": "♝"},
    "king": {"black": "♔", "white": "♚"},
    "queen": {"black": "♕", "white": "♛"},
    "pawn": {"black": "♙", "white": "♟"}
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
        if move.piece.color == "white" and move.destination[1] == 0:
            pass
        return True
    def moveLit(self, lit):
        charToX = {
            "A": 0,
            "B": 1,
            "C": 2,
            "D": 3,
            "E": 4,
            "F": 5,
            "G": 6,
            "H": 7
        }
        charToY = [8, 7, 6, 5, 4, 3, 2, 1]
        movArray = lit.strip(" ")
        movArray = [char for char in movArray]
        origin = (charToX[movArray[0]], charToY[int(movArray[1])])
        destination = (charToX[movArray[2]], charToY[int(movArray[3])])
        self.move(move(self.board, self.board.layout[origin[1]][origin[0]], origin, destination, self.board.layout[destination[1]][destination[0]]))
    def isGameOver(self):
        if len(self.legalMoves()) == 0:
            checkMate = False
            for mov in self.legalMoves(all = True):
                if mov.eats:
                    if mov.eats.type == "king" and mov.eats.color == self.turn:
                        checkMate = True
                        wonCodes = {
                            "black": "White wins",
                            "white": "Black wins"
                        }
                        return wonCodes[self.turn]
            if not checkMate:
                return "Stalemate"
        return False
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
                    if piec.type == "knight" and checkColor(all, self.turn, piec):
                        for x in range(-2, 3):
                            for y in range(-2, 3):
                                if abs(x) == abs(y) or x == 0 or y == 0:
                                    continue
                                if case[1]+y <= 7 and case[1]+y >=0 and case[0]+x <= 7 and case[0]+x >= 0:
                                    if self.board.layout[case[1]+y][case[0]+x] == None:
                                        moves.append(move(self.board, piec, case, (case[0]+x, case[1]+y)))
                                    else:
                                        if self.board.layout[case[1]+y][case[0]+x].color != piec.color:
                                            moves.append(move(self.board, piec, case, (case[0]+x, case[1]+y), self.board.layout[case[1]+y][case[0]+x]))
                    if piec.type == "pawn" and checkColor(all, self.turn, piec):
                        if piec.color == "black":
                            if case[1]+1 <= 7:
                                if self.board.layout[case[1]+1][case[0]] == None:
                                    moves.append(move(self.board, piec, case, (case[0], case[1]+1)))
                                    if case[1] == 1:
                                        if self.board.layout[case[1]+2][case[0]] == None:
                                            moves.append(move(self.board, piec, case, (case[0], case[1]+2)))
                            for x in range(-1, 2):
                                if x == 0:
                                    continue
                                if case[0]+x >= 0 and case[0]+x <= 7 and case[1]+1 <= 7 and self.board.layout[case[1]+1][case[0]+x] != None:
                                    if self.board.layout[case[1]+1][case[0]+x].color != piec.color:
                                        moves.append(move(self.board, piec, case, (case[0]+x, case[1]+1), self.board.layout[case[1]+1][case[0]+x]))
                        else:
                            if case[1]-1 >= 0:
                                if self.board.layout[case[1]-1][case[0]] == None:
                                    moves.append(move(self.board, piec, case, (case[0], case[1]-1)))
                                    if case[1] == 6:
                                        if self.board.layout[case[1]-2][case[0]] == None:
                                            moves.append(move(self.board, piec, case, (case[0], case[1]-2)))
                            for x in range(-1, 2):
                                if x == 0:
                                    continue
                                if case[0]+x >= 0 and case[0]+x <= 7 and case[1]-1 <= 7 and self.board.layout[case[1]-1][case[0]+x] != None:
                                    if self.board.layout[case[1]-1][case[0]+x].color != piec.color:
                                        moves.append(move(self.board, piec, case, (case[0]+x, case[1]-1), self.board.layout[case[1]-1][case[0]+x]))
                    if piec.type == "king" and checkColor(all, self.turn, piec):
                        for x in range(-1, 2):
                            for y in range(-1, 2):
                                if abs(x) == abs(y) and abs(x) == 0:
                                    continue
                                if case[1]+y <= 7 and case[1]+y >=0 and case[0]+x <= 7 and case[0]+x >= 0:
                                    if self.board.layout[case[1]+y][case[0]+x] == None:
                                        moves.append(move(self.board, piec, case, (case[0]+x, case[1]+y)))
                                    else:
                                        if self.board.layout[case[1]+y][case[0]+x].color != piec.color:
                                            moves.append(move(self.board, piec, case, (case[0]+x, case[1]+y), self.board.layout[case[1]+y][case[0]+x]))
                    if piec.type == "queen" and checkColor(all, self.turn, piec):
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
    def __init__(self, board = [[piece("rook", "black"), piece("knight", "black"), piece("bishop", "black"), piece("queen", "black"), piece("king", "black"), piece("bishop", "black"), piece("knight", "black"), piece("rook", "black")], [piece("pawn", "black"), piece("pawn", "black"), piece("pawn", "black"), piece("pawn", "black"), piece("pawn", "black"), piece("pawn", "black"), piece("pawn", "black"), piece("pawn", "black")], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [piece("pawn", "white"), piece("pawn", "white"), piece("pawn", "white"), piece("pawn", "white"), piece("pawn", "white"), piece("pawn", "white"), piece("pawn", "white"), piece("pawn", "white")], [piece("rook", "white"), piece("knight", "white"), piece("bishop", "white"), piece("queen", "white"), piece("king", "white"), piece("bishop", "white"), piece("knight", "white"), piece("rook", "white")]]):
        self.layout = board
    def printBoard(self):
        print("  A;B;C;D;E;F;G;H")
        rowN = 8
        for row in self.layout:
            print(str(rowN)+" ", end="")
            for piec in row:
                if piec:
                    print(lettersName[piec.type][piec.color], end=";")
                else:
                    print(" ", end=";")
            print()
            rowN -= 1
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
                    if piec.type == "knight":
                        for x in range(-2, 3):
                            for y in range(-2, 3):
                                if abs(x) == abs(y) or x == 0 or y == 0:
                                    continue
                                if case[1]+y <= 7 and case[1]+y >=0 and case[0]+x <= 7 and case[0]+x >= 0:
                                    if self.layout[case[1]+y][case[0]+x] == None:
                                        moves.append(move(self, piec, case, (case[0]+x, case[1]+y)))
                                    else:
                                        if self.layout[case[1]+y][case[0]+x].color != piec.color:
                                            moves.append(move(self, piec, case, (case[0]+x, case[1]+y), self.layout[case[1]+y][case[0]+x]))
                    if piec.type == "pawn":
                        if piec.color == "black":
                            if case[1]+1 <= 7:
                                if self.layout[case[1]+1][case[0]] == None:
                                    moves.append(move(self, piec, case, (case[0], case[1]+1)))
                                    if case[1] == 1:
                                        if self.layout[case[1]+2][case[0]] == None:
                                            moves.append(move(self, piec, case, (case[0], case[1]+2)))
                            for x in range(-1, 2):
                                if x == 0:
                                    continue
                                if case[0]+x >= 0 and case[0]+x <= 7 and case[1]+1 <= 7 and self.layout[case[1]+1][case[0]+x] != None:
                                    if self.layout[case[1]+1][case[0]+x].color != piec.color:
                                        moves.append(move(self, piec, case, (case[0]+x, case[1]+1), self.layout[case[1]+1][case[0]+x]))
                        else:
                            if case[1]-1 >= 0:
                                if self.layout[case[1]-1][case[0]] == None:
                                    moves.append(move(self, piec, case, (case[0], case[1]-1)))
                                    if case[1] == 6:
                                        if self.layout[case[1]-2][case[0]] == None:
                                            moves.append(move(self, piec, case, (case[0], case[1]-2)))
                            for x in range(-1, 2):
                                if x == 0:
                                    continue
                                if case[0]+x >= 0 and case[0]+x <= 7 and case[1]-1 <= 7 and self.layout[case[1]-1][case[0]+x] != None:
                                    if self.layout[case[1]-1][case[0]+x].color != piec.color:
                                        moves.append(move(self, piec, case, (case[0]+x, case[1]-1), self.layout[case[1]-1][case[0]+x]))
                    if piec.type == "king":
                        for x in range(-2, 3):
                            for y in range(-2, 3):
                                if abs(x) == abs(y) or x == 0 or y == 0:
                                    continue
                                if case[1]+y <= 7 and case[1]+y >=0 and case[0]+x <= 7 and case[0]+x >= 0:
                                    if self.layout[case[1]+y][case[0]+x] == None:
                                        moves.append(move(self, piec, case, (case[0]+x, case[1]+y)))
                                    else:
                                        if self.layout[case[1]+y][case[0]+x].color != piec.color:
                                            moves.append(move(self, piec, case, (case[0]+x, case[1]+y), self.layout[case[1]+y][case[0]+x]))
                    if piec.type == "queen":
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
        legalMoves = theGame.legalMoves()
        if theGame.isGameOver():
            reasonOfEnd = theGame.isGameOver()
            break
        print("Available moves:")
        for i in legalMoves:
            print("---")
            print(index0)
            print(i.piece.type)
            print(i.toStr())
            i.simulate().printBoard()
            index0 += 1
        print("The current board:")
        print(theGame.turn + "'s turn")
        theGame.board.printBoard()
        litMoves = []
        for i in legalMoves:
            litMoves.append(i.toStr())
        index = ""
        while not index in litMoves:
            index = input().upper()
            if not index in litMoves:
                print("Move not allowed")
        theGame.moveLit(index)
    print(reasonOfEnd)
    theGame.board.printBoard()
