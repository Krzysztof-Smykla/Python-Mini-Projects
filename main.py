# Building a 2048 game using the Pygame library
import pygame
import random

pygame.init()

WIDTH = 400
HEIGHT = 500

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('2048')
timer = pygame.time.Clock()
fps = 70
font = pygame.font.SysFont('Calibri', 24)

# 2048 game color library:
colors = {0: (204, 192, 179),
          2: (238, 228, 218),
          4: (237, 224, 200),
          8: (242, 177, 121),
          16: (245, 149, 99),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (237, 207, 114),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 194, 46),
          'light text': (249, 246, 242),
          'dark text': (119, 110, 101),
          'other': (255, 0, 212),  # purple
          'bg': (177, 173, 160)}

# Initialize game variables
board_values = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
spawn_new = True
init_count = 0
direction = ''
# Keeping score
score = 0
file = open('high_score', 'r')
init_high = int(file.readline())
file.close()
high_score = init_high


# Take your turn based on direction
def take_turn(direc, board):
    global score
    merged = [[False for _ in range(4)] for _ in range(4)]
    if direc == 'UP':
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        # Update vacant square to 0
                        board[i][j] = 0
                    # Check if two pieces [i] amd [i-1] have equal values
                    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift - 1][j] \
                            and not merged[i - shift][j]:
                        board[i - shift - 1][j] *= 2
                        # Update score
                        score += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True

    elif direc == 'DOWN':
        for j in range(4):
            for i in range(2, -1, -1):  # Start from second last row to the top
                if board[i][j] != 0:
                    k = i
                    while k < 3 and board[k + 1][j] == 0:
                        board[k + 1][j] = board[k][j]
                        board[k][j] = 0
                        k += 1
                    if k < 3 and board[k + 1][j] == board[k][j] and not merged[k + 1][j] and not merged[k][j]:
                        board[k + 1][j] *= 2
                        # Update score
                        score += board[k + 1][j]
                        board[k][j] = 0
                        merged[k + 1][j] = True
    elif direc == 'LEFT':
        for i in range(4):
            for j in range(1, 4):  # Start from second column
                if board[i][j] != 0:
                    k = j
                    while k > 0 and board[i][k - 1] == 0:
                        board[i][k - 1] = board[i][k]
                        board[i][k] = 0
                        k -= 1
                    if k > 0 and board[i][k - 1] == board[i][k] and not merged[i][k - 1] and not \
                            merged[i][k]:
                        board[i][k - 1] *= 2
                        # Update score
                        score += board[i][k - 1]
                        board[i][k] = 0
                        merged[i][k - 1] = True

    elif direc == 'RIGHT':
        for i in range(4):
            for j in range(2, -1, -1):  # Start from third column to the left
                if board[i][j] != 0:
                    k = j
                    while k < 3 and board[i][k + 1] == 0:
                        board[i][k + 1] = board[i][k]
                        board[i][k] = 0
                        k += 1
                    if k < 3 and board[i][k + 1] == board[i][k] and not merged[i][k + 1] and not merged[i][k]:
                        board[i][k + 1] *= 2
                        # Update score
                        score += board[i][k + 1]
                        board[i][k] = 0
                        merged[i][k + 1] = True

    return board


# spawn in new pieces randomly when turn starts
def new_pieces(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
        if count < 1:
            full = True
    return board, full


# draw background for the board
def draw_board():
    pygame.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)
    score_text = font.render(f'Score: {score}', True, 'black')
    high_score_text = font.render(f'High Score: {high_score}', True, 'black')
    screen.blit(score_text, (10, 410))
    screen.blit(high_score_text, (10, 450))
    pass


# draw tiles for game
def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']

            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
            if value > 0:
                value_len = len(str(value))
                value_font = pygame.font.SysFont('Calibri', 48 - (5 * value_len), bold=True)
                value_text = value_font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, 'black', [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)


# Draw game over and restart text
def draw_over():
    pygame.draw.rect(screen, 'black', [50, 50, 300, 100], 0, 10)
    game_over_text1 = font.render('Game Over!', True, 'white')
    game_over_text2 = font.render("Press ENTER to Restart", True, 'white')
    screen.blit(game_over_text1, (130, 65))
    screen.blit(game_over_text2, (70, 105))


def check_game_over(board):
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                return False  # Empty space means possible move
            # Check all four directions for possible merges
            if i > 0 and board[i][j] == board[i - 1][j]:
                return False
            if i < 3 and board[i][j] == board[i + 1][j]:
                return False
            if j > 0 and board[i][j] == board[i][j - 1]:
                return False
            if j < 3 and board[i][j] == board[i][j + 1]:
                return False
    return True  # No moves left


# main game loop
run = True
while run:
    timer.tick(fps)
    screen.fill('gray')
    draw_board()
    draw_pieces(board_values)
    if spawn_new or init_count < 2:
        board_values, _ = new_pieces(board_values)  # Don't assign to game_over here
        spawn_new = False
        init_count += 1

    if direction != '':
        board_values = take_turn(direction, board_values)
        direction = ''
        spawn_new = True

    if check_game_over(board_values):
        game_over = True

    if game_over:
        draw_over()
        if high_score > init_high:
            file = open('high_score', 'w')
            file.write(f'{high_score}')
            file.close()
            init_high = high_score

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                direction = 'UP'
            elif event.key == pygame.K_DOWN:
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT:
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                direction = 'RIGHT'
        # Reinitialize game on game over
        if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
            board_values = [[0 for _ in range(4)] for _ in range(4)]
            spawn_new = True
            init_count = 0
            score = 0
            direction = ''
            game_over = False

    if score > high_score:
        high_score = score

    pygame.display.flip()
pygame.quit()
