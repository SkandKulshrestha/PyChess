from typing import List


class ChessState:
    KNIGHT_DIRECTION = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                        (1, -2), (1, 2), (2, -1), (2, 1)]

    #                   up-left
    BISHOP_DIRECTION = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    #                   up      left     down   right
    ROOK_DIRECTION = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    QUEEN_DIRECTION = BISHOP_DIRECTION + ROOK_DIRECTION
    KING_DIRECTION = BISHOP_DIRECTION + ROOK_DIRECTION

    def __init__(self):
        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],  # Rank 8
            ['p'] * 8,  # Rank 7
            [''] * 8,  # Rank 6
            [''] * 8,  # Rank 5
            [''] * 8,  # Rank 4
            [''] * 8,  # Rank 3
            ['P'] * 8,  # Rank 2
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],  # Rank 1
        ]
        self.white_to_move = True
        self.move_log = list()

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = ''
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured

    def get_valid_moves(self):
        return self.get_all_possible_moves()

    def get_all_possible_moves(self):
        moves = list()

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and ((self.white_to_move and piece.isupper()) or (not self.white_to_move and piece.islower())):
                    get_piece_move = eval(f'self.get_{piece.lower()}_moves')
                    get_piece_move(row, col, moves)

        return moves

    def is_enemy(self, piece):
        return piece.islower() if self.white_to_move else piece.isupper()

    def get_p_moves(self, row: int, col: int, moves: List):
        start_square = (row, col)
        if self.white_to_move:
            direction = -1
            starting_rank = 6
        else:
            direction = 1
            starting_rank = 1

        # advance possible
        end_row = row + direction
        if self.board[end_row][col] == '':
            # 1 square pawn advance
            moves.append(Move(start_square, (end_row, col), self.board))
        end_row += direction
        if row == starting_rank and self.board[end_row][col] == '':
            # 2 square pawn advance from starting rank
            moves.append(Move(start_square, (end_row, col), self.board))

        # capture possible
        end_row = row + direction
        if col - 1 >= 0:
            # left capture possible
            if self.is_enemy(self.board[end_row][col - 1]):
                moves.append(Move(start_square, (end_row, col - 1), self.board))
        if col + 1 <= 7:
            # right capture possible
            if self.is_enemy(self.board[end_row][col + 1]):
                moves.append(Move(start_square, (end_row, col + 1), self.board))

    def get_n_moves(self, row: int, col: int, moves: List):
        start_square = (row, col)
        for d in self.KNIGHT_DIRECTION:
            end_row = row + d[0]
            end_col = col + d[1]

            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                if end_piece == '' or self.is_enemy(end_piece):
                    # empty space => advance => valid move
                    # enemy piece => capture => valid move
                    # friendly piece => illegal move
                    moves.append(Move(start_square, (end_row, end_col), self.board))

    def get_b_r_q_moves(self, row: int, col: int, moves: List, direction: List):
        start_square = (row, col)
        for d in direction:
            for i in range(1, 8):
                end_row = row + d[0] * i
                end_col = col + d[1] * i

                if end_row < 0 or end_row > 7 or end_col < 0 or end_col > 7:
                    # out of chess board
                    break

                end_piece = self.board[end_row][end_col]
                if end_piece == '':
                    # empty space => advance => valid move
                    moves.append(Move(start_square, (end_row, end_col), self.board))
                elif self.is_enemy(end_piece):
                    # enemy piece => capture => valid move
                    moves.append(Move(start_square, (end_row, end_col), self.board))
                    break
                else:
                    # friendly piece => illegal move
                    break

    def get_b_moves(self, row: int, col: int, moves: List):
        self.get_b_r_q_moves(row, col, moves, self.BISHOP_DIRECTION)

    def get_r_moves(self, row: int, col: int, moves: List):
        self.get_b_r_q_moves(row, col, moves, self.ROOK_DIRECTION)

    def get_q_moves(self, row: int, col: int, moves: List):
        self.get_b_r_q_moves(row, col, moves, self.QUEEN_DIRECTION)

    def get_k_moves(self, row: int, col: int, moves: List):
        start_square = (row, col)
        for d in self.KING_DIRECTION:
            end_row = row + d[0]
            end_col = col + d[1]

            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                if end_piece == '' or self.is_enemy(end_piece):
                    # empty space => advance => valid move
                    # enemy piece => capture => valid move
                    # friendly piece => illegal move
                    moves.append(Move(start_square, (end_row, end_col), self.board))


class Move:
    ROW_TO_RANK = {0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}
    COL_TO_FILE = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

    def __init__(self, start_square, end_square, board):
        self.start_row, self.start_col = start_square
        self.end_row, self.end_col = end_square
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_id = (self.start_row << 12) | (self.start_col << 8) | (self.end_row << 4) | self.end_col

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id

    def get_chess_notation(self, long_algebraic_notation: bool = False) -> str:
        result = self.piece_moved if self.piece_moved.upper() != 'P' else ''

        if long_algebraic_notation:
            result += self.get_file_rank(self.start_row, self.start_col)
            result += 'x' if self.piece_captured else '-'
            result += self.get_file_rank(self.end_row, self.end_col)
        else:
            # TODO: Handle disambiguating moves
            if self.piece_captured:
                if self.piece_moved.upper() == 'P':
                    result += self.get_file(self.start_col)
                result += 'x'
            result += self.get_file_rank(self.end_row, self.end_col)

        return result

    def get_file_rank(self, row, col):
        return self.COL_TO_FILE[col] + self.ROW_TO_RANK[row]

    def get_file(self, col):
        return self.COL_TO_FILE[col]

    def get_rank(self, row):
        return self.ROW_TO_RANK[row]
