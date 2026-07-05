#!/usr/bin/env python3
import sys, json
sys.path.insert(0, '/home/mettaclaw/artifacts')
from connect4_dumb import new_board, drop_piece, choose_ai_move, legal_moves, winner, print_board
SF = '/home/mettaclaw/artifacts/c4_state.json'
def load_state():
    try:
        with open(SF) as f: return json.load(f)
    except: return {'board': new_board(), 'turn': 'O'}
def save_state(s):
    with open(SF, 'w') as f: json.dump({'board': s['board'], 'turn': s['turn']}, f)
if len(sys.argv) < 2: print('Usage: c4_game.py [new|move COL|ai|show]'); sys.exit(1)
cmd = sys.argv[1]
if cmd == 'new':
    s = {'board': new_board(), 'turn': 'O'}; save_state(s); print_board(s['board']); print('New game. You are O.')
elif cmd == 'show':
    s = load_state(); print_board(s['board']); print(f"Turn: {s['turn']}")
elif cmd == 'move':
    col = int(sys.argv[2]); s = load_state()
    if s['turn'] != 'O': print('Not your turn!'); sys.exit(1)
    if col not in legal_moves(s['board']): print('Illegal!'); sys.exit(1)
    drop_piece(s['board'], col, 'O')
    w = winner(s['board'])
    if w: print_board(s['board']); print(f'{w} wins!'); save_state(s); sys.exit(0)
    if not legal_moves(s['board']): print_board(s['board']); print('Draw!'); save_state(s); sys.exit(0)
    s['turn'] = 'X'; save_state(s); print_board(s['board'])
elif cmd == 'ai':
    s = load_state()
    if s['turn'] != 'X': print('Not AI turn!'); sys.exit(1)
    ac = choose_ai_move(s['board'])
    if ac is None: print('Draw!'); sys.exit(0)
    drop_piece(s['board'], ac, 'X')
    w = winner(s['board'])
    if w: print_board(s['board']); print(f'{w} wins!'); save_state(s); sys.exit(0)
    if not legal_moves(s['board']): print_board(s['board']); print('Draw!'); save_state(s); sys.exit(0)
    s['turn'] = 'O'; save_state(s); print_board(s['board']); print(f'AI played col {ac}')