import time

import pygame
import ChessEngine

from typing import Tuple, List

SQUARE_LENGTH = 64
RANK = FILE = DIMENSION = 8
BOARD_LENGTH = SQUARE_LENGTH * DIMENSION
MAX_FPS = 15
IMAGES = {}
POSITION = []
COLORS = [pygame.Color('white'), pygame.Color('gray')]


def load_and_transform(image_path: str):
    return pygame.transform.scale(pygame.image.load(image_path), (SQUARE_LENGTH, SQUARE_LENGTH))


def load_images():
    global IMAGES
    for piece in ('P', 'N', 'B', 'R', 'Q', 'K'):
        # load white pieces, i.e., 'P', 'N', 'B', 'R', 'Q', and 'K'
        IMAGES[piece] = load_and_transform(f"images/w{piece}.png")

        # load black pieces, i.e., 'p', 'n', 'b', 'r', 'q', and 'k'
        IMAGES[piece.lower()] = load_and_transform(f"images/b{piece}.png")


def load_positions():
    global POSITION
    row_to_rank = {0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}
    col_to_file = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
    # my_font = pygame.font.SysFont('Comic Sans MS', 10)
    my_font = pygame.font.SysFont('Times New Roman', 15)
    for row in range(RANK):
        _position = []
        for col in range(FILE):
            _position.append(my_font.render(col_to_file[col] + row_to_rank[row], False, (0, 0, 0)))
        POSITION.append(_position)


def draw_board(chess_window):
    for row in range(RANK):
        for col in range(FILE):
            color = COLORS[(row + col) % 2]
            pygame.draw.rect(chess_window, color,
                             pygame.Rect(col * SQUARE_LENGTH, row * SQUARE_LENGTH, SQUARE_LENGTH, SQUARE_LENGTH))
            chess_window.blit(POSITION[row][col],
                              pygame.Rect(col * SQUARE_LENGTH, row * SQUARE_LENGTH, SQUARE_LENGTH, SQUARE_LENGTH))


def draw_pieces(chess_window, board):
    for row in range(RANK):
        for col in range(FILE):
            piece = board[row][col]
            if piece:
                chess_window.blit(IMAGES[piece],
                                  pygame.Rect(col * SQUARE_LENGTH, row * SQUARE_LENGTH, SQUARE_LENGTH, SQUARE_LENGTH))


def draw_chess_state(chess_window, chess_state):
    draw_board(chess_window)
    draw_pieces(chess_window, chess_state.board)


def main():
    # create chess board
    pygame.init()
    chess_window = pygame.display.set_mode((BOARD_LENGTH, BOARD_LENGTH))
    pygame.display.set_caption('Chess')
    icon = pygame.image.load('images/chess.png')
    pygame.display.set_icon(icon)

    # chess_window.fill(pygame.Color('white'))
    clock = pygame.time.Clock()

    # load chess configuration
    running: bool = True
    square_selected: Tuple[int, int] = tuple()
    player_clicks: List[Tuple[int, int]] = list()
    load_images()
    load_positions()

    # create an instance of Chess
    chess_state = ChessEngine.ChessState()
    start = time.perf_counter()
    valid_moves = chess_state.get_valid_moves()
    end = time.perf_counter()
    print(f'Time take to analyze valid moves: {end - start}')
    print(f'{chess_state.turn_to_move()} can move {valid_moves}')
    move_made = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit event is triggered
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # MouseButtonDown event is triggered
                # get row and column numbers
                location = pygame.mouse.get_pos()
                col = location[0] // SQUARE_LENGTH
                row = location[1] // SQUARE_LENGTH
                _square_selected = (row, col)

                if _square_selected == square_selected:
                    # same square is selected
                    # undo the selection
                    square_selected = tuple()
                    player_clicks.clear()
                else:
                    square_selected = _square_selected
                    player_clicks.append(square_selected)

                print('-' * 80)
                print(player_clicks)
                print(chess_state.turn_to_move())

                if len(player_clicks) == 2:
                    # player has clicked two times
                    move = ChessEngine.Move(*player_clicks, chess_state.board)
                    if move in valid_moves:
                        print(move)
                        chess_state.make_move(move)
                        move_made = True
                        square_selected = tuple()
                        player_clicks.clear()
                    else:
                        player_clicks = [_square_selected]

            elif event.type == pygame.KEYDOWN:
                # KeyDown event is triggered
                if event.key == pygame.K_z:
                    # Key press Z
                    chess_state.undo_move()
                    move_made = True

            else:
                pass

            if move_made:
                print('Valid move made')
                start = time.perf_counter()
                valid_moves = chess_state.get_valid_moves()
                end = time.perf_counter()
                print(f'Time take to analyze valid moves: {end - start}')
                print(f'{chess_state.turn_to_move()} can move {valid_moves}')
                move_made = False

        draw_chess_state(chess_window, chess_state)
        clock.tick(MAX_FPS)
        pygame.display.flip()

        if len(valid_moves) == 0:
            if chess_state.checkmate:
                print('Check Mate')
            else:
                print('Stalemate')


if __name__ == '__main__':
    main()
