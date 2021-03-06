'''
 This class is responsible for storing all the information about the current state of a chess game.
 It will also be responsible for determining the valid moves at the current state.
 It will also keep a move log
'''

import chessMain

class GameState():
    def __init__(self):
        # Board is an 8x8 2d list, each element of the list has 2 character.
        # the first character represents the color of the piece, 'b' or 'w'
        # the second character represents the type of the piece 'k', 'q', 'r', 'b', 'n', 'p'
        self.board =[
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wK", "wK", "wK", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        
    '''
    Takes a Move as a parameter and executes it (this will not work for castling, pawn promotion, ans en - passant)
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove # swap players
    '''
    Undo the last move made
    '''
    def undoMove(self):
        if len(self.moveLog) != 0: # make sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # switch turn back

    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        return self.getAllPossibleMoves() # for now we will not worry about checks

    '''
    All moves without considering checks
    '''

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): # number of rows
            for c in range(len(self.board[r])): # number of cols in given row
                pieceState = self.board[r][c][0]
                if ( pieceState == 'w' and self.whiteToMove ) or ( pieceState == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) # calls the appropriate move function based on piece type
        return moves

    '''
    Get all the pawn moves for the pawn located at row, col and these moves to the list
    '''

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: # white pawn move
            if self.board[r-1][c] == "--": # 1 square pawn advance
                moves.append(Move((r,c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--": # 2 square pawn advance
                    moves.append(Move((r, c), (r-2, c), self.board))

            if c-1 >= 0:  # captures to the left
                if self.board[r-1][c-1][0] == 'b': # enemy piece to capture
                    moves.append(Move((r, c), (r-1 ,c-1), self.board))
            if c+1 <= 7:  # captures to the right
                if self.board[r-1][c+1][0] == 'b': # enemy piece to capture
                    moves.append(Move((r, c), (r-1, c+1), self.board))



        else: # black pawn moves
            if self.board[r+1][c] == "--": # 1 square pawn advance
                moves.append(Move((r,c), (r+1,c), self.board))
                if r == 1 and self.board[r+2][c] == "--": # 2 square pawn advance
                    moves.append(Move((r,c), (r+2, c), self.board))

            if c-1 >= 0: # captures to the right
                if self.board[r+1][c-1][0] == 'w': # enemy piece to capture
                    moves.append(Move((r,c), (r+1, c-1), self.board))

            if c+1 <= 7: # captures to the left
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r,c), (r+1, c+1), self.board))

        # add pawn promotions later

    '''
    Get all the Rook moves for the Rook located at roe, col and add these moves to the list
    '''

    def getRookMoves(self, r, c, moves):
        directions = ((-1,0), (0,-1), (1,0), (0,1))
        enemyColor = "b" if self.whiteToMove else "w"

        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": # empty space valid
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: # enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: # friendly piece invalid
                        break
                else: # off board
                    break


    '''
    Get all the Knight moves for the Knight located at roe, col and add these moves to the list
    '''

    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1)) # 4 dimensions
        allyColor = 'w' if self.whiteToMove else 'b'

        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: # empty or enemy color piece
                    moves.append(Move((r,c), (endRow, endCol), self.board))



    '''
    Get all the Bishop moves for the Bishop located at roe, col and add these moves to the list
    '''

    def getBishopMoves(self, r, c, moves):
        directions = ((-1,-1), (-1,1), (1,-1), (1,1)) # 4 dimensions
        enemyColor = 'b' if self.whiteToMove else 'w'

        for d in directions:
            for i in range(1, 8): # bishop can move max 7 sqaure
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": # empty space valid
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: # enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: # friendly piece invalid
                        break
                else: # off board
                    break

    '''
    Get all the Queen moves for the Queen located at roe, col and add these moves to the list
    '''

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)
        self.getKnightMoves(r,c,moves)
    '''
    Get all the King moves for the King located at roe, col and add these moves to the list
    '''

    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1,-1), (-1,0), (-1,1), (0,-1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: # not an ally piece (empty or enemy piece)
                    moves.append(Move((r, c), (endRow, endCol), self.board))



class Move():
    # maps keys to values
    # key : value

    ranksToRows = {"1": 7, "2":6, "3": 5, "4": 4, "5":3, "6": 2, "7":1, "8": 0}

    rowsToRanks = {v : k for k, v in ranksToRows.items()}

    filesToCols = {"a" : 0, "b": 1, "c": 2, "d":3, "e":4, "f":5, "g":6, "h":7}

    colsToFiles = {v: k for k, v in filesToCols.items()}
     
    def __init__(self, startSq, endSq, board):
      self.startRow = startSq[0]
      self.startCol = startSq[1]
      self.endRow = endSq[0]
      self.endCol = endSq[1]
      self.pieceMoved = board[self.startRow][self.startCol]
      self.pieceCaptured = board[self.endRow][self.endCol]
      self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol


    '''
    Overriding the equal method
    '''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]



