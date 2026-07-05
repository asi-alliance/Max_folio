#!/usr/bin/env python3
import os
import random

ROWS = 6
COLS = 7

EMPTY = " "
HUMAN = "O"
AI = "X"

def env_float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, str(default)))
    except ValueError:
        return default

AI_TAKE_WIN_PROB = env_float("AI_TAKE_WIN_PROB", 0.33)
AI_BLOCK_PROB = env_float("AI_BLOCK_PROB", 0.33)
AI_CENTER_PROB = env_float("AI_CENTER_PROB", 0.33)

def new_board():
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print(" 0 1 2 3 4 5 6")
    print("---------------")
    for row in board:
        print("|" + "|".join(row) + "|")
    print("---------------")
    print()

def legal_moves(board):
    return [c for c in range(COLS) if board[0][c] == EMPTY]

def drop_piece(board, col, piece):
    if col not in legal_moves(board):
        return False
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            board[r][col] = piece
            return True
    return False

def winner(board):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(ROWS):
        for c in range(COLS):
            piece = board[r][c]
            if piece == EMPTY:
                continue
            for dr, dc in directions:
                ok = True
                for i in range(4):
                    rr = r + dr * i
                    cc = c + dc * i
                    if rr < 0 or rr >= ROWS or cc < 0 or cc >= COLS:
                        ok = False
                        break
                    if board[rr][cc] != piece:
                        ok = False
                        break
                if ok:
                    return piece
    return None

def would_win(board, col, piece):
    test = [row[:] for row in board]
    if not drop_piece(test, col, piece):
        return False
    return winner(test) == piece

def choose_ai_move(board):
    moves = legal_moves(board)
    if not moves:
        return None
    if random.random() < AI_TAKE_WIN_PROB:
        immediate_wins = [c for c in moves if would_win(board, c, AI)]
        if immediate_wins:
            return random.choice(immediate_wins)
    if random.random() < AI_BLOCK_PROB:
        immediate_blocks = [c for c in moves if would_win(board, c, HUMAN)]
        if immediate_blocks:
            return random.choice(immediate_blocks)
    if random.random() < AI_CENTER_PROB:
        for c in [3, 2, 4, 1, 5, 0, 6]:
            if c in moves:
                return c
    return random.choice(moves)

def read_column():
    while True:
        try:
            raw = input("Enter a column: ").strip()
        except EOFError:
            raise
        try:
            col = int(raw)
        except ValueError:
            print("Please enter a number from 0 to 6.")
            continue
        if 0 <= col <= 6:
            return col
        print("Please enter a number from 0 to 6.")

def main():
    board = new_board()
    print("Medium-dumb Connect Four")
    print(f"Human/LLM: {HUMAN}")
    print(f"AI:        {AI}")
    print()
    print("AI settings:")
    print(f"  AI_TAKE_WIN_PROB = {AI_TAKE_WIN_PROB}")
    print(f"  AI_BLOCK_PROB    = {AI_BLOCK_PROB}")
    print(f"  AI_CENTER_PROB   = {AI_CENTER_PROB}")
    print()
    while True:
        print_board(board)
        while True:
            col = read_column()
            if drop_piece(board, col, HUMAN):
                break
            print("That column is full.")
        w = winner(board)
        if w:
            print_board(board)
            print(f"{w} wins!")
            return
        if not legal_moves(board):
            print_board(board)
            print("Draw.")
            return
        print_board(board)
        print("AI is thinking about a move...")
        print()
        ai_col = choose_ai_move(board)
        if ai_col is None:
            print_board(board)
            print("Draw.")
            return
        drop_piece(board, ai_col, AI)
        w = winner(board)
        if w:
            print_board(board)
            print(f"{w} wins!")
            return
        if not legal_moves(board):
            print_board(board)
            print("Draw.")
            return

if __name__ == "__main__":
    main()