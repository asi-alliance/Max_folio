import numpy as np

class Connect4Env:
    ROWS = 6
    COLS = 7
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = 2

    def __init__(self):
        self.board = np.zeros((self.ROWS, self.COLS), dtype=int)
        self.current_player = self.PLAYER1
        self.game_over = False
        self.winner = None
        self.move_history = []
        self.trace = []

    def drop_piece(self, col):
        if col < 0 or col >= self.COLS or self.game_over:
            return False
        for row in range(self.ROWS - 1, -1, -1):
            if self.board[row][col] == self.EMPTY:
                self.board[row][col] = self.current_player
                self.move_history.append((row, col, self.current_player))
                self.trace.append({
                    'move_num': len(self.move_history),
                    'player': self.current_player,
                    'col': col,
                    'row': row,
                    'board_before': None,
                    'board_after': self.board.copy()
                })
                if self.check_win(row, col):
                    self.game_over = True
                    self.winner = self.current_player
                elif len(self.legal_moves()) == 0:
                    self.game_over = True
                    self.winner = 0
                self.current_player = 3 - self.current_player
                return True
        return False

    def legal_moves(self):
        return [c for c in range(self.COLS) if self.board[0][c] == self.EMPTY]

    def check_win(self, row, col):
        player = self.board[row][col]
        directions = [(0,1),(1,0),(1,1),(1,-1)]
        for dr, dc in directions:
            count = 1
            for sign in [1, -1]:
                r, c = row + sign*dr, col + sign*dc
                while 0 <= r < self.ROWS and 0 <= c < self.COLS and self.board[r][c] == player:
                    count += 1
                    r += sign*dr
                    c += sign*dc
            if count >= 4:
                return True
        return False

    def display(self):
        symbols = {0: '.', 1: 'X', 2: 'O'}
        lines = []
        for row in self.board:
            lines.append(' '.join(symbols[c] for c in row))
        lines.append(' '.join(str(i) for i in range(self.COLS)))
        return chr(10).join(lines)

    def get_board_state(self):
        return self.board.copy(), self.current_player, self.game_over, self.winner