import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("TicTacToe")
clock = pygame.time.Clock()

GOLD = '#E88817'
GREEN = '#008264'
rows = 3
cols = 3
blocks = []
current_player = 'X'
font = pygame.font.Font(None, 74)
clock = pygame.time.Clock()

def make_the_board():
    global blocks
    blocks = []
    for i in range(rows):
        for j in range(cols):
            block = pygame.Surface((200, 200))
            block.fill('White')
            block_rect = block.get_rect(topleft=(j * 200, i * 200))
            blocks.append((block, block_rect))

def draw_outline(block_rect):
    pygame.draw.rect(screen, 'Black', block_rect, 2)

def draw_the_board():
    for block, block_rect in blocks:
        screen.blit(block, block_rect)
        draw_outline(block_rect)

def draw_the_moves(board):
    for i in range(rows):
        for j in range(cols):
            if board[i][j] == 'X':
                x_surface = pygame.image.load('tictactoe/x.jpeg').convert_alpha()
                x_surface = pygame.transform.scale(x_surface, (200, 200))
                block, block_rect = blocks[i * cols + j]
                blocks[i * cols + j] = (x_surface, block_rect)
            elif board[i][j] == 'O':
                o_surface = pygame.image.load('tictactoe/o.jpeg').convert_alpha()
                o_surface = pygame.transform.scale(o_surface, (200, 200))
                block, block_rect = blocks[i * cols + j]
                blocks[i * cols + j] = (o_surface, block_rect)

def winning(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != '':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != '':
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '':
        return board[0][2]
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                return 'None'
    return 'Draw'

def display_winner(winner):
    global restart_rect, start_state_rect 

    screen.fill('White')
    if winner != 'Draw':
        text = font.render(f'{winner} wins', True, 'Black')
    else:
        text = font.render(f'{winner} !', True, 'Black')    
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    screen.blit(text, text_rect)
    
    restart_surface = pygame.Surface((300, 150))
    restart_surface.fill(GREEN)
    restart_rect = restart_surface.get_rect(center=(screen_width / 2 - 150, screen_height / 2 + 50))
    screen.blit(restart_surface, restart_rect)
    restart_text = font.render("Restart", True, (255, 255, 255))
    restart_text_rect = restart_text.get_rect(center=restart_rect.center)
    screen.blit(restart_text, restart_text_rect)

    start_state_surface = pygame.Surface((300, 150))
    start_state_surface.fill(GOLD)
    start_state_rect = start_state_surface.get_rect(center=(screen_width / 2 + 150, screen_height / 2 + 50))
    screen.blit(start_state_surface, start_state_rect)
    start_state_text = font.render("Main Menu", True, (255, 255, 255))
    start_state_text_rect = start_state_text.get_rect(center=start_state_rect.center)
    screen.blit(start_state_text, start_state_text_rect)

    return restart_rect, start_state_rect

def setup_screen():
    screen.fill('Black')
    
    two_player_surface = pygame.Surface((300, 150))
    two_player_surface.fill(GREEN)
    two_player_rect = two_player_surface.get_rect(center=(screen_width / 2 - 150, screen_height / 2))
    screen.blit(two_player_surface, two_player_rect)
    two_player_text = font.render("Two Player", True, (255, 255, 255))
    two_player_text_rect = two_player_text.get_rect(center=two_player_rect.center)
    screen.blit(two_player_text, two_player_text_rect)

    one_player_surface = pygame.Surface((300, 150))
    one_player_surface.fill(GOLD)
    one_player_rect = one_player_surface.get_rect(center=(screen_width / 2 + 150, screen_height / 2))
    screen.blit(one_player_surface, one_player_rect)
    one_player_text = font.render("One Player", True, (255, 255, 255))
    one_player_text_rect = one_player_text.get_rect(center=one_player_rect.center)
    screen.blit(one_player_text, one_player_text_rect)

    return two_player_rect, one_player_rect

two_player_rect , one_player_rect = setup_screen()
make_the_board()
matrix = [['' for _ in range(cols)] for _ in range(rows)]
game_state = 'start'
mode = ''

def board_to_string(board):
    board_str = ''
    for i in range(len(board)):
        for j in range(len(board[i])):
            board_str += board[i][j]
    return board_str

def MiniMax(board, depth, is_maximizing):
    winner = winning(board)
    if winner == 'X':
        return 1, depth
    elif winner == 'O':
        return -1, depth
    elif winner == 'Draw':
        return 0, depth

    if is_maximizing:
        best_score = -float('inf')
        best_depth = float('inf')
        for i in range(rows):
            for j in range(cols):
                if board[i][j] == '':
                    board[i][j] = 'X'
                    score, depth = MiniMax(board, depth + 1, False)
                    board[i][j] = ''
                    if score > best_score or (score == best_score and depth < best_depth):
                        best_score = score
                        best_depth = depth
        return best_score, best_depth
    else:
        best_score = float('inf')
        best_depth = float('inf')
        for i in range(rows):
            for j in range(cols):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    score, depth = MiniMax(board, depth + 1, True)
                    board[i][j] = ''
                    if score < best_score or (score == best_score and depth < best_depth):
                        best_score = score
                        best_depth = depth
        return best_score, best_depth

def best_move(board):
    best_score = float('inf')
    best_depth = float('inf')
    move = None
    for i in range(rows):
        for j in range(cols):
            if board[i][j] == '':
                board[i][j] = 'O'
                score, depth = MiniMax(board, 0, True)
                board[i][j] = ''
                if score < best_score or (score == best_score and depth < best_depth):
                    best_score = score
                    best_depth = depth
                    move = (i, j)
    return move


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN and game_state == 'playing':
            if mode == 'two':
                for i in range(rows):
                    for j in range(cols):
                        index = i * cols + j
                        if blocks[index][1].collidepoint(event.pos):
                            if matrix[i][j] == '':
                                matrix[i][j] = current_player
                                current_player = 'O' if current_player == 'X' else 'X'
            elif mode == 'one' and current_player == 'X':
                for i in range(rows):
                    for j in range(cols):
                        index = i * cols + j
                        if blocks[index][1].collidepoint(event.pos):
                            if matrix[i][j] == '':
                                matrix[i][j] = current_player
                                # AI's move here
                                current_player = 'O'
                                move = best_move(matrix)
                                if move:
                                    matrix[move[0]][move[1]] = 'O'
                                    current_player = 'X'
                                    
        elif event.type == pygame.MOUSEBUTTONDOWN and game_state == 'gameover':
            if start_state_rect and start_state_rect.collidepoint(event.pos):
                matrix = [['' for _ in range(cols)] for _ in range(rows)]
                game_state = 'start'
            elif restart_rect and restart_rect.collidepoint(event.pos):
                matrix = [['' for _ in range(cols)] for _ in range(rows)]
                make_the_board()
                game_state = 'playing'
                      
        elif event.type == pygame.MOUSEBUTTONDOWN and game_state == 'start':
            if two_player_rect and two_player_rect.collidepoint(event.pos):
                make_the_board()
                mode = 'two'
                game_state = 'playing'
            elif one_player_rect and one_player_rect.collidepoint(event.pos):
                make_the_board()
                mode = 'one'
                game_state = 'playing'
    
    if game_state == 'start':
        setup_screen()
    
    else:
        draw_the_board()
        draw_the_moves(matrix)
        winner = winning(matrix)
        if winner != 'None':
            game_state = 'gameover'
            current_player = 'X'
            restart_rect, start_state_rect = display_winner(winner)
        
    pygame.display.flip()
    clock.tick(60)
