import copy
import pygame

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
        yToChar = ["8", "7", "6", "5", "4", "3", "2", "1"]
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
        charToY = [7, 6, 5, 4, 3, 2, 1, 0]
        movArray = lit.strip(" ")
        movArray = [char for char in movArray]
        origin = (charToX[movArray[0]], charToY[int(movArray[1])-1])
        destination = (charToX[movArray[2]], charToY[int(movArray[3])-1])
        if self.board.layout[origin[1]][origin[0]].type == "pawn" and self.board.layout[origin[1]][origin[0]].color == "black" and origin[1] == 6:
            print("1) Queen")
            print("2) Bishop")
            print("3) Knight")
            print("4) Rook")
            print("Please choose transformation")
            choice = 0
            while 1 > choice or choice > 4:
                choice = int(input())
            trTypes = ["queen", "bishop", "knight", "rook"]
            choice = trTypes[choice - 1]
            self.move(move(self.board, piece(choice, self.turn), origin, destination, self.board.layout[destination[1]][destination[0]]))
        else:
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
                                    if 1 != case[1] !=6:
                                        moves.append(move(self.board, piec, case, (case[0], case[1]+1)))
                                    if case[1] == 1:
                                        if self.board.layout[case[1]+2][case[0]] == None:
                                            moves.append(move(self.board, piec, case, (case[0], case[1]+2)))
                                    if case[1] == 6:
                                        if self.board.layout[case[1]+1][case[0]] == None:
                                            for type in ["rook", "knight", "bishop", "queen"]:
                                                moves.append(move(self.board, piece(type, "black"), case, (case[0], case[1]+1)))
                            for x in range(-1, 2):
                                if x == 0:
                                    continue
                                if case[0]+x >= 0 and case[0]+x <= 7 and case[1]+1 <= 7 and self.board.layout[case[1]+1][case[0]+x] != None:
                                    if self.board.layout[case[1]+1][case[0]+x].color != piec.color:    
                                        if case[1] != 6:
                                            moves.append(move(self.board, piec, case, (case[0]+x, case[1]+1), self.board.layout[case[1]+1][case[0]+x]))
                                        else:
                                            if self.board.layout[case[1]+1][case[0]] == None:
                                                for type in ["rook", "knight", "bishop", "queen"]:
                                                    moves.append(move(self.board, piece(type, "black"), case, (case[0]+x, case[1]+1), self.board.layout[case[1]+1][case[0]+x]))
                        else:
                            if case[1]-1 >= 0:
                                if self.board.layout[case[1]-1][case[0]] == None:
                                    if 1 != case[1] !=6:
                                        moves.append(move(self.board, piec, case, (case[0], case[1]-1)))
                                    if case[1] == 6:
                                        if self.board.layout[case[1]-2][case[0]] == None:
                                            moves.append(move(self.board, piec, case, (case[0], case[1]-2)))
                                    if case[1] == 1:
                                        if self.board.layout[case[1]-1][case[0]] == None:
                                            for type in ["rook", "knight", "bishop", "queen"]:
                                                moves.append(move(self.board, piece(type, "white"), case, (case[0], case[1]-1)))
                            for x in range(-1, 2):
                                if x == 0:
                                    continue
                                if case[0]+x >= 0 and case[0]+x <= 7 and case[1]-1 <= 7 and self.board.layout[case[1]-1][case[0]+x] != None:
                                    if self.board.layout[case[1]-1][case[0]+x].color != piec.color:
                                        if case[1] != 1:
                                            moves.append(move(self.board, piec, case, (case[0]+x, case[1]-1), self.board.layout[case[1]+1][case[0]+x]))
                                        else:
                                            if self.board.layout[case[1]-1][case[0]] == None:
                                                for type in ["rook", "knight", "bishop", "queen"]:
                                                    moves.append(move(self.board, piece(type, "white"), case, (case[0]+x, case[1]-1), self.board.layout[case[1]-1][case[0]+x]))
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
                                    if 1 != case[1] !=6:
                                        moves.append(move(self, piec, case, (case[0], case[1]+1)))
                                    if case[1] == 1:
                                        if self.layout[case[1]+2][case[0]] == None:
                                            moves.append(move(self, piec, case, (case[0], case[1]+2)))
                                    if case[1] == 6:
                                        if self.layout[case[1]+1][case[0]] == None:
                                            for type in ["rook", "knight", "bishop", "queen"]:
                                                moves.append(move(self, piece(type, "black"), case, (case[0], case[1]+1)))
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
                                        if case[1] != 6:
                                            moves.append(move(self, piec, case, (case[0]+x, case[1]-1), self.layout[case[1]-1][case[0]+x]))
                                        else:
                                            if self.layout[case[1]-1][case[0]] == None:
                                                for type in ["rook", "knight", "bishop", "queen"]:
                                                    moves.append(move(self, piece(type, "white"), case, (case[0]+x, case[1]-1), self.layout[case[1]-1][case[0]+x]))
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
    pygame.init()
    dispw = 800
    disph = 800

    display = pygame.display.set_mode((dispw, disph))
    pygame.display.set_caption('Échecs du club de coding EIB Étoile')
    #icon = pygame.image.load(resource_path('./images/icon.png'))
    #pygame.display.set_icon(icon)
    clock = pygame.time.Clock()
    pygame.font.init()
    myfont = pygame.font.SysFont('Times New Roman', 30)
    game_over = False
    newBoard = board([[piece("rook", "black"), None, None, None, None, None, None, None], [None, piece("pawn", "white"), None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, piece("pawn", "white"), None, None, None, None], [None, None, None, None, piece("pawn", "black"), None, None, None], [None, None, None, piece("rook", "white"), None, None, None, None]])
    theGame = game(newBoard)
    cases = {
        "a8": pygame.Rect((0, 0), (100, 100)),
        "b8": pygame.Rect((100, 0), (100, 100)),
        "c8": pygame.Rect((200, 0), (100, 100)),
        "d8": pygame.Rect((300, 0), (100, 100)),
        "e8": pygame.Rect((400, 0), (100, 100)),
        "f8": pygame.Rect((500, 0), (100, 100)),
        "g8": pygame.Rect((600, 0), (100, 100)),
        "h8": pygame.Rect((700, 0), (100, 100)),
        "a7": pygame.Rect((0, 100), (100, 100)),
        "b7": pygame.Rect((100, 100), (100, 100)),
        "c7": pygame.Rect((200, 100), (100, 100)),
        "d7": pygame.Rect((300, 100), (100, 100)),
        "e7": pygame.Rect((400, 100), (100, 100)),
        "f7": pygame.Rect((500, 100), (100, 100)),
        "g7": pygame.Rect((600, 100), (100, 100)),
        "h7": pygame.Rect((700, 100), (100, 100)),
        "a6": pygame.Rect((0, 200), (100, 100)),
        "b6": pygame.Rect((100, 200), (100, 100)),
        "c6": pygame.Rect((200, 200), (100, 100)),
        "d6": pygame.Rect((300, 200), (100, 100)),
        "e6": pygame.Rect((400, 200), (100, 100)),
        "f6": pygame.Rect((500, 200), (100, 100)),
        "g6": pygame.Rect((600, 200), (100, 100)),
        "h6": pygame.Rect((700, 200), (100, 100)),
        "a5": pygame.Rect((0, 300), (100, 100)),
        "b5": pygame.Rect((100, 300), (100, 100)),
        "c5": pygame.Rect((200, 300), (100, 100)),
        "d5": pygame.Rect((300, 300), (100, 100)),
        "e5": pygame.Rect((400, 300), (100, 100)),
        "f5": pygame.Rect((500, 300), (100, 100)),
        "g5": pygame.Rect((600, 300), (100, 100)),
        "h5": pygame.Rect((700, 300), (100, 100)),
        "a4": pygame.Rect((0, 400), (100, 100)),
        "b4": pygame.Rect((100, 400), (100, 100)),
        "c4": pygame.Rect((200, 400), (100, 100)),
        "d4": pygame.Rect((300, 400), (100, 100)),
        "e4": pygame.Rect((400, 400), (100, 100)),
        "f4": pygame.Rect((500, 400), (100, 100)),
        "g4": pygame.Rect((600, 400), (100, 100)),
        "h4": pygame.Rect((700, 400), (100, 100)),
        "a3": pygame.Rect((0, 500), (100, 100)),
        "b3": pygame.Rect((100, 500), (100, 100)),
        "c3": pygame.Rect((200, 500), (100, 100)),
        "d3": pygame.Rect((300, 500), (100, 100)),
        "e3": pygame.Rect((400, 500), (100, 100)),
        "f3": pygame.Rect((500, 500), (100, 100)),
        "g3": pygame.Rect((600, 500), (100, 100)),
        "h3": pygame.Rect((700, 500), (100, 100)),
        "a2": pygame.Rect((0, 600), (100, 100)),
        "b2": pygame.Rect((100, 600), (100, 100)),
        "c2": pygame.Rect((200, 600), (100, 100)),
        "d2": pygame.Rect((300, 600), (100, 100)),
        "e2": pygame.Rect((400, 600), (100, 100)),
        "f2": pygame.Rect((500, 600), (100, 100)),
        "g2": pygame.Rect((600, 600), (100, 100)),
        "h2": pygame.Rect((700, 600), (100, 100)),
        "a1": pygame.Rect((0, 700), (100, 100)),
        "b1": pygame.Rect((100, 700), (100, 100)),
        "c1": pygame.Rect((200, 700), (100, 100)),
        "d1": pygame.Rect((300, 700), (100, 100)),
        "e1": pygame.Rect((400, 700), (100, 100)),
        "f1": pygame.Rect((500, 700), (100, 100)),
        "g1": pygame.Rect((600, 700), (100, 100)),
        "h1": pygame.Rect((700, 700), (100, 100)),
    }
    selectedCase = None
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for index, case in cases.items():
                    if case.collidepoint(event.pos):
                        selectedCase = case
        display.fill((0, 0, 0))
        
        pygame.draw.rect(display, (255, 206, 158), cases["a8"])
        pygame.draw.rect(display, (209, 139, 71), cases["a7"])
        pygame.draw.rect(display, (255, 206, 158), cases["a6"])
        pygame.draw.rect(display, (209, 139, 71), cases["a5"])
        pygame.draw.rect(display, (255, 206, 158), cases["a4"])
        pygame.draw.rect(display, (209, 139, 71), cases["a3"])
        pygame.draw.rect(display, (255, 206, 158), cases["a2"])
        pygame.draw.rect(display, (209, 139, 71), cases["a1"])
        pygame.draw.rect(display, (209, 139, 71), cases["b8"])
        pygame.draw.rect(display, (255, 206, 158), cases["b7"])
        pygame.draw.rect(display, (209, 139, 71), cases["b6"])
        pygame.draw.rect(display, (255, 206, 158), cases["b5"])
        pygame.draw.rect(display, (209, 139, 71), cases["b4"])
        pygame.draw.rect(display, (255, 206, 158), cases["b3"])
        pygame.draw.rect(display, (209, 139, 71), cases["b2"])
        pygame.draw.rect(display, (255, 206, 158), cases["b1"])
        pygame.draw.rect(display, (255, 206, 158), cases["c8"])
        pygame.draw.rect(display, (209, 139, 71), cases["c7"])
        pygame.draw.rect(display, (255, 206, 158), cases["c6"])
        pygame.draw.rect(display, (209, 139, 71), cases["c5"])
        pygame.draw.rect(display, (255, 206, 158), cases["c4"])
        pygame.draw.rect(display, (209, 139, 71), cases["c3"])
        pygame.draw.rect(display, (255, 206, 158), cases["c2"])
        pygame.draw.rect(display, (209, 139, 71), cases["c1"])
        pygame.draw.rect(display, (209, 139, 71), cases["d8"])
        pygame.draw.rect(display, (255, 206, 158), cases["d7"])
        pygame.draw.rect(display, (209, 139, 71), cases["d6"])
        pygame.draw.rect(display, (255, 206, 158), cases["d5"])
        pygame.draw.rect(display, (209, 139, 71), cases["d4"])
        pygame.draw.rect(display, (255, 206, 158), cases["d3"])
        pygame.draw.rect(display, (209, 139, 71), cases["d2"])
        pygame.draw.rect(display, (255, 206, 158), cases["d1"])
        pygame.draw.rect(display, (255, 206, 158), cases["e8"])
        pygame.draw.rect(display, (209, 139, 71), cases["e7"])
        pygame.draw.rect(display, (255, 206, 158), cases["e6"])
        pygame.draw.rect(display, (209, 139, 71), cases["e5"])
        pygame.draw.rect(display, (255, 206, 158), cases["e4"])
        pygame.draw.rect(display, (209, 139, 71), cases["e3"])
        pygame.draw.rect(display, (255, 206, 158), cases["e2"])
        pygame.draw.rect(display, (209, 139, 71), cases["e1"])
        pygame.draw.rect(display, (209, 139, 71), cases["f8"])
        pygame.draw.rect(display, (255, 206, 158), cases["f7"])
        pygame.draw.rect(display, (209, 139, 71), cases["f6"])
        pygame.draw.rect(display, (255, 206, 158), cases["f5"])
        pygame.draw.rect(display, (209, 139, 71), cases["f4"])
        pygame.draw.rect(display, (255, 206, 158), cases["f3"])
        pygame.draw.rect(display, (209, 139, 71), cases["f2"])
        pygame.draw.rect(display, (255, 206, 158), cases["f1"])
        pygame.draw.rect(display, (255, 206, 158), cases["g8"])
        pygame.draw.rect(display, (209, 139, 71), cases["g7"])
        pygame.draw.rect(display, (255, 206, 158), cases["g6"])
        pygame.draw.rect(display, (209, 139, 71), cases["g5"])
        pygame.draw.rect(display, (255, 206, 158), cases["g4"])
        pygame.draw.rect(display, (209, 139, 71), cases["g3"])
        pygame.draw.rect(display, (255, 206, 158), cases["g2"])
        pygame.draw.rect(display, (209, 139, 71), cases["g1"])
        pygame.draw.rect(display, (209, 139, 71), cases["h8"])
        pygame.draw.rect(display, (255, 206, 158), cases["h7"])
        pygame.draw.rect(display, (209, 139, 71), cases["h6"])
        pygame.draw.rect(display, (255, 206, 158), cases["h5"])
        pygame.draw.rect(display, (209, 139, 71), cases["h4"])
        pygame.draw.rect(display, (255, 206, 158), cases["h3"])
        pygame.draw.rect(display, (209, 139, 71), cases["h2"])
        pygame.draw.rect(display, (255, 206, 158), cases["h1"])
        
        if selectedCase:
            pygame.draw.rect(display, (0, 255, 0), selectedCase,  2)

        pygame.display.update()

        clock.tick(30)
