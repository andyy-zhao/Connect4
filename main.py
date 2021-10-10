import numpy as np
import pygame
import sys
import math

# global variables (static variables are capitalized to show that they are a non-changing variable)
BLUE = (0, 50, 255) # RGB Value
BLACK = (0, 0, 0) 
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7


pygame.init()

# create a zero matrix 6 by 7
def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece): 
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    # command in numpy
    print(np.flip(board, 0)) # 0 is the axis

def winning_move(board, piece):
    # checking all horizontal locations
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    
    # checking all vertical locations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    
    # checking positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # checking negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            # drawing blue rectangles
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE)) #size of width and height, and position of the rectangle. c * squaresize is the top left corner, r * squaresize is position on y axis, h and w are squaresize
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), RADIUS)
        
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)
    pygame.display.update()

board = create_board()
print_board(board)
# game_over set to True when 4 in a row is obtained
game_over = False 
turn = 0


SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)
# circle radius
RADIUS = int(SQUARESIZE / 2 - 5) # divide by 2 because you want radius not diameter

screen = pygame.display.set_mode(size)

#draw board draws the board
draw_board(board)
pygame.display.update() #whenever you want to update your display 

myfont = pygame.font.SysFont("monospace", 75)



while not game_over:
    # events include mouse click, arrow keys, movements
    for event in pygame.event.get():
        # always include this
        if event.type == pygame.QUIT:
            sys.exit()

        # show player 
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0] #constantly updating
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()

        # drop a piece by clicking down
        if event.type == pygame.MOUSEBUTTONDOWN:
            # print(event.pos)
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            # player 1 input 
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = myfont.render("Player 1 wins!", 1, RED)
                        screen.blit(label, (40,10)) # updates specific part of screen
                        game_over = True

            # player 2 input4
            else:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        label = myfont.render("Player 2 wins!", 1, YELLOW)
                        screen.blit(label, (40,10)) # updates specific part of screen
                        game_over = True
            
            print_board(board)
            draw_board(board)
                
            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(3000)
