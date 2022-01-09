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
    def status(self):
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
        return "Playing"
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
                                    if 0 != case[1] != 7:
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
                                    if 0 != case[1] != 7:
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
                                    if 0 != case[1] != 7:
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
                                if 0 != case[1] != 7:
                                        moves.append(move(self, piec, case, (case[0], case[1]-1)))
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
                        for x in range(-1, 2):
                            for y in range(-1, 2):
                                if abs(x) == abs(y) and abs(x) == 0:
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

lettersName = {
    "rook": {"black": "♖", "white": "♜"},
    "knight": {"black": "♘", "white": "♞"},
    "bishop": {"black": "♗", "white": "♝"},
    "king": {"black": "♔", "white": "♚"},
    "queen": {"black": "♕", "white": "♛"},
    "pawn": {"black": "♙", "white": "♟"}
}

def writeText(text, color, pos, highlighted):
    textsurface = myfont.render(text, False, color)
    textRect = textsurface.get_rect()
    textRect.topleft = (pos)
    if highlighted:
        pygame.draw.rect(dis, (75, 75, 75), textRect)
    display.blit(textsurface, textRect)

if __name__ == "__main__":
    pygame.init()
    dispw = 800
    disph = 900

    display = pygame.display.set_mode((dispw, disph))
    pygame.display.set_caption('Chess AI of the EIB Étoile coding club')
    icon = pygame.image.load('./images/icon.png')
    pygame.display.set_icon(icon)
    #icon = pygame.image.load(resource_path('./images/icon.png'))
    #pygame.display.set_icon(icon)
    clock = pygame.time.Clock()
    pygame.font.init()
    myfont = pygame.font.SysFont('Times New Roman', 30)
    game_over = False
    newBoard = board()
    theGame = game(newBoard)
    tiles = {
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
    pieces = {
        "rook": {"black": pygame.image.load("./images/rookb.png").convert_alpha(), "white": pygame.image.load("./images/rookw.png").convert_alpha()},
        "knight": {"black": pygame.image.load("./images/knightb.png").convert_alpha(), "white": pygame.image.load("./images/knightw.png").convert_alpha()},
        "bishop": {"black": pygame.image.load("./images/bishopb.png").convert_alpha(), "white": pygame.image.load("./images/bishopw.png").convert_alpha()},
        "king": {"black": pygame.image.load("./images/kingb.png").convert_alpha(), "white": pygame.image.load("./images/kingw.png").convert_alpha()},
        "queen": {"black": pygame.image.load("./images/queenb.png").convert_alpha(), "white": pygame.image.load("./images/queenw.png").convert_alpha()},
        "pawn": {"black": pygame.image.load("./images/pawnb.png").convert_alpha(), "white": pygame.image.load("./images/pawnw.png").convert_alpha()}
    }
    selectedCase = None
    selectedCaseName = None
    while not game_over:
        moved = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for index, case in tiles.items():
                    if case.collidepoint(event.pos):
                        for movement in theGame.legalMoves():
                            if movement.toStr("x").split("x")[1].lower() == index and movement.toStr("x").split("x")[0].lower() == selectedCaseName:
                                theGame.move(movement)
                                moved = True
                        if not moved:
                            selectedCase = case
                            selectedCaseName = index
        display.fill((255, 255, 255))
        
        pygame.draw.rect(display, (255, 206, 158), tiles["a8"])
        pygame.draw.rect(display, (209, 139, 71), tiles["a7"])
        pygame.draw.rect(display, (255, 206, 158), tiles["a6"])
        pygame.draw.rect(display, (209, 139, 71), tiles["a5"])
        pygame.draw.rect(display, (255, 206, 158), tiles["a4"])
        pygame.draw.rect(display, (209, 139, 71), tiles["a3"])
        pygame.draw.rect(display, (255, 206, 158), tiles["a2"])
        pygame.draw.rect(display, (209, 139, 71), tiles["a1"])
        pygame.draw.rect(display, (209, 139, 71), tiles["b8"])
        pygame.draw.rect(display, (255, 206, 158), tiles["b7"])
        pygame.draw.rect(display, (209, 139, 71), tiles["b6"])
        pygame.draw.rect(display, (255, 206, 158), tiles["b5"])
        pygame.draw.rect(display, (209, 139, 71), tiles["b4"])
        pygame.draw.rect(display, (255, 206, 158), tiles["b3"])
        pygame.draw.rect(display, (209, 139, 71), tiles["b2"])
        pygame.draw.rect(display, (255, 206, 158), tiles["b1"])
        pygame.draw.rect(display, (255, 206, 158), tiles["c8"])
        pygame.draw.rect(display, (209, 139, 71), tiles["c7"])
        pygame.draw.rect(display, (255, 206, 158), tiles["c6"])
        pygame.draw.rect(display, (209, 139, 71), tiles["c5"])
        pygame.draw.rect(display, (255, 206, 158), tiles["c4"])
        pygame.draw.rect(display, (209, 139, 71), tiles["c3"])
        pygame.draw.rect(display, (255, 206, 158), tiles["c2"])
        pygame.draw.rect(display, (209, 139, 71), tiles["c1"])
        pygame.draw.rect(display, (209, 139, 71), tiles["d8"])
        pygame.draw.rect(display, (255, 206, 158), tiles["d7"])
        pygame.draw.rect(display, (209, 139, 71), tiles["d6"])
        pygame.draw.rect(display, (255, 206, 158), tiles["d5"])
        pygame.draw.rect(display, (209, 139, 71), tiles["d4"])
        pygame.draw.rect(display, (255, 206, 158), tiles["d3"])
        pygame.draw.rect(display, (209, 139, 71), tiles["d2"])
        pygame.draw.rect(display, (255, 206, 158), tiles["d1"])
        pygame.draw.rect(display, (255, 206, 158), tiles["e8"])
        pygame.draw.rect(display, (209, 139, 71), tiles["e7"])
        pygame.draw.rect(display, (255, 206, 158), tiles["e6"])
        pygame.draw.rect(display, (209, 139, 71), tiles["e5"])
        pygame.draw.rect(display, (255, 206, 158), tiles["e4"])
        pygame.draw.rect(display, (209, 139, 71), tiles["e3"])
        pygame.draw.rect(display, (255, 206, 158), tiles["e2"])
        pygame.draw.rect(display, (209, 139, 71), tiles["e1"])
        pygame.draw.rect(display, (209, 139, 71), tiles["f8"])
        pygame.draw.rect(display, (255, 206, 158), tiles["f7"])
        pygame.draw.rect(display, (209, 139, 71), tiles["f6"])
        pygame.draw.rect(display, (255, 206, 158), tiles["f5"])
        pygame.draw.rect(display, (209, 139, 71), tiles["f4"])
        pygame.draw.rect(display, (255, 206, 158), tiles["f3"])
        pygame.draw.rect(display, (209, 139, 71), tiles["f2"])
        pygame.draw.rect(display, (255, 206, 158), tiles["f1"])
        pygame.draw.rect(display, (255, 206, 158), tiles["g8"])
        pygame.draw.rect(display, (209, 139, 71), tiles["g7"])
        pygame.draw.rect(display, (255, 206, 158), tiles["g6"])
        pygame.draw.rect(display, (209, 139, 71), tiles["g5"])
        pygame.draw.rect(display, (255, 206, 158), tiles["g4"])
        pygame.draw.rect(display, (209, 139, 71), tiles["g3"])
        pygame.draw.rect(display, (255, 206, 158), tiles["g2"])
        pygame.draw.rect(display, (209, 139, 71), tiles["g1"])
        pygame.draw.rect(display, (209, 139, 71), tiles["h8"])
        pygame.draw.rect(display, (255, 206, 158), tiles["h7"])
        pygame.draw.rect(display, (209, 139, 71), tiles["h6"])
        pygame.draw.rect(display, (255, 206, 158), tiles["h5"])
        pygame.draw.rect(display, (209, 139, 71), tiles["h4"])
        pygame.draw.rect(display, (255, 206, 158), tiles["h3"])
        pygame.draw.rect(display, (209, 139, 71), tiles["h2"])
        pygame.draw.rect(display, (255, 206, 158), tiles["h1"])
        
        for y in range(len(theGame.board.layout)):
            for x in range(len(theGame.board.layout[y])):
                tile = theGame.board.layout[y][x]
                if tile:
                    try:
                        display.blit(pieces[tile.type][tile.color], tiles[chr(x+97)+str(8-y)])
                    except:
                        continue
        if selectedCase:
            if theGame.board.layout[8-int(selectedCaseName[1])][ord(selectedCaseName[0])-97]:
                if theGame.board.layout[8-int(selectedCaseName[1])][ord(selectedCaseName[0])-97].color == theGame.turn:
                    pygame.draw.rect(display, (0, 255, 0), selectedCase,  2)
                    for movement in theGame.legalMoves():
                        if theGame.board.layout[movement.origin[1]][movement.origin[0]] == theGame.board.layout[8-int(selectedCaseName[1])][ord(selectedCaseName[0])-97]:
                            pygame.draw.circle(display, (0, 255, 0), tiles[movement.toStr("x").split("x")[1].lower()].center, 15, 0)
                else:
                    pygame.draw.rect(display, (255, 0, 0), selectedCase,  2)
                    for movement in theGame.board.legalMoves():
                        if theGame.board.layout[movement.origin[1]][movement.origin[0]] == theGame.board.layout[8-int(selectedCaseName[1])][ord(selectedCaseName[0])-97]:
                            pygame.draw.circle(display, (255, 0, 0), tiles[movement.toStr("x").split("x")[1].lower()].center, 15, 0)
        
        writeText("Turn: {}".format(theGame.turn), (0, 0, 0), (10, 805), False)
        writeText("Number of turns: {}".format(theGame.nTurn), (0, 0, 0), (10, 830), False)
        writeText("Game status: {}".format(theGame.status()), (0, 0, 0), (10, 855), False)
        
        pygame.display.update()

        if theGame.isGameOver():
            break
        clock.tick(30)

while not game_over:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True