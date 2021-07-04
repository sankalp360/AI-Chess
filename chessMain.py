'''this is our main driver file.
 It will be responsible for handling user input and
 displaying the current GameState object.
'''
import pygame as p
import chessEngine
import images



WIDTH = HEIGHT = 512 # 400 is another option

DIMENSION = 8 # dimensions of chess board are 8x8

SQ_SIZE = HEIGHT // DIMENSION

MAX_FPS = 15 #for animations later on

IMAGES = {}

# NOT LOADING IMAGES EVERYTIME AND LOADING IT IN A GLOBAL DICTIONARY OF IMAGES

def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


    # Note we can acess an image by saying 'IMAGES['wp']'

'''
The main driver for our code. this will handle user input and updating the graphics

'''

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False  # flag variable for when a move is made


    # print(gs.board)
    loadImages() # only once before the while loop
    running = True
    sqSelected = ()  # no square is selected , keep track of the last click of the user (tuple: (row, col))
    playerClicks = []  # keep track of the player clicks (two tuples:[(6, 4)-->(4, 4)])

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # tuple : (x, y) location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):  # the user clicked the same sqaure twice
                    sqSelected = ()  # deselect
                    playerClicks = []  # clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)  # append for both 1st and 2nd clicks
                
                if len(playerClicks)==2:  # after 2nd click
                    move = chessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = ()  #reset user clicks
                    playerClicks = []

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

# Responsible for all graphics within a current game state

def drawGameState(screen, gs):
    drawBoard(screen) # draw squares on the board
    drawPieces(screen, gs.board) # draw pieces on the top of those sqaures

# Draw the sqaure on the board. The top left sqaure is always light.

def drawBoard(screen):
    colors = [p.Color("white"), p.Color("grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Draw the pieces on the board using the current GameStare.board            

def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if(piece != "--"): # not empty sqaure
                screen.blit(IMAGES[piece], p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            




if __name__ == "__main__":
    main()