"""
MAXWORLD Wrapper - Clean API for agent interaction with the MAXWORLD grid world.

Usage:
    from wrapper import MaxWorld
    
    world = MaxWorld('./maxworld')
    board = world.observe()        # Returns list of strings (the grid)
    world.move('right')            # Execute a move, returns new board
    world.reset()                  # Reset to initial state
    state = world.read_state()     # Read raw JSON state dict
    world.write_state(state)       # Write raw JSON state (for counterfactual tasks)
    world.action_history()         # Returns list of actions taken
"""

import subprocess
import json
import os
import shutil
import tempfile


class MaxWorld:
    """Wrapper around the maxworld binary providing a clean API."""
    
    VALID_ACTIONS = ['up', 'down', 'left', 'right', 'reset']
    
    def __init__(self, binary_path='./maxworld', work_dir=None, state_file='.myworld_state.json'):
        """Initialize the MAXWORLD wrapper.
        
        Args:
            binary_path: Path to the maxworld binary.
            work_dir: Working directory for the agent (default: current dir).
            state_file: Name of the state file (default: .myworld_state.json).
        """
        self.binary_path = os.path.abspath(binary_path)
        self.work_dir = work_dir or os.getcwd()
        self.state_file = os.path.join(self.work_dir, state_file)
        self._history = []
        self._step_count = 0
        
        if not os.path.exists(self.binary_path):
            raise FileNotFoundError(f"MaxWorld binary not found: {self.binary_path}")
    
    def observe(self):
        """Return the current board as a list of strings (one per row)."""
        result = subprocess.run(
            [self.binary_path],
            capture_output=True, text=True, cwd=self.work_dir, timeout=10
        )
        if result.returncode != 0:
            raise RuntimeError(f"maxworld failed: {result.stderr}")
        return result.stdout.strip().split('\n')
    
    def move(self, direction):
        """Execute a move and return the new board.
        
        Args:
            direction: One of 'up', 'down', 'left', 'right'.
            
        Returns:
            List of strings representing the new board state.
        """
        direction = direction.lower().strip()
        if direction not in self.VALID_ACTIONS:
            raise ValueError(f"Invalid action: {direction}. Must be one of {self.VALID_ACTIONS}")
        
        self._history.append(direction)
        self._step_count += 1
        
        result = subprocess.run(
            [self.binary_path, direction],
            capture_output=True, text=True, cwd=self.work_dir, timeout=10
        )
        if result.returncode != 0:
            raise RuntimeError(f"maxworld {direction} failed: {result.stderr}")
        return result.stdout.strip().split('\n')
    
    def reset(self):
        """Reset the world to its initial state. Returns the reset board."""
        self._history.append('reset')
        result = subprocess.run(
            [self.binary_path, 'reset'],
            capture_output=True, text=True, cwd=self.work_dir, timeout=10
        )
        if result.returncode != 0:
            raise RuntimeError(f"maxworld reset failed: {result.stderr}")
        return result.stdout.strip().split('\n')
    
    def read_state(self):
        """Read the raw JSON state file.
        
        Returns:
            Dict with key 'world' containing a list of row strings.
        """
        if not os.path.exists(self.state_file):
            raise FileNotFoundError(f"State file not found: {self.state_file}")
        with open(self.state_file, 'r') as f:
            return json.load(f)
    
    def write_state(self, state):
        """Write a raw state dict to the state file.
        
        This enables counterfactual tasks (save-file editing).
        
        Args:
            state: Dict with key 'world' containing a list of row strings.
        """
        if 'world' not in state:
            raise ValueError("State must have a 'world' key")
        with open(self.state_file, 'w') as f:
            json.dump(state, f)
    
    def action_history(self):
        """Return the list of actions taken so far."""
        return list(self._history)
    
    def step_count(self):
        """Return the number of non-reset actions taken."""
        return sum(1 for a in self._history if a != 'reset')
    
    def find_glyph(self, glyph, board=None):
        """Find all positions of a glyph on the board.
        
        Args:
            glyph: The character(s) to search for.
            board: Board to search (default: current state).
            
        Returns:
            List of (row, col) tuples.
        """
        if board is None:
            board = self.observe()
        positions = []
        for row_idx, row in enumerate(board):
            col_idx = 0
            for ch in row:
                if ch == glyph:
                    positions.append((row_idx, col_idx))
                col_idx += 1
        return positions
    
    def get_board_diff(self, board_before, board_after):
        """Compare two boards and return list of (row, col, before, after) changes."""
        diffs = []
        for r in range(min(len(board_before), len(board_after))):
            for c in range(min(len(board_before[r]), len(board_after[r]))):
                if board_before[r][c] != board_after[r][c]:
                    diffs.append((r, c, board_before[r][c], board_after[r][c]))
        return diffs
    
    def save_state_copy(self, path):
        """Save a copy of the current state file to the given path."""
        shutil.copy2(self.state_file, path)
    
    def restore_state_copy(self, path):
        """Restore state from a saved copy."""
        shutil.copy2(path, self.state_file)
