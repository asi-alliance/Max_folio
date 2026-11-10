#!/usr/bin/env python3
"""
Example MAXWORLD Agent

This is a minimal agent that explores MAXWORLD by trying random moves.
Replace the `solve` function with your own logic.

Your agent must define:
    solve(world, task) -> dict

Where:
    world: MaxWorld instance (see wrapper.py)
    task: dict with task parameters (see tasks/*.json)

Return a dict with at minimum:
    'completed': bool
    'steps_taken': int
    
And for Level 1:
    'discovered_mechanics': list of mechanism name strings
"""

import random


def solve(world, task):
    level = task['level']
    
    if level == 1:
        return solve_explore(world, task)
    elif level == 2:
        return solve_navigate(world, task)
    elif level == 3:
        return solve_deliver(world, task)
    elif level == 4:
        return solve_optimize(world, task)
    elif level == 5:
        return solve_counterfactual(world, task)
    else:
        return {'completed': False, 'steps_taken': 0}


def solve_explore(world, task):
    """Level 1: Discover mechanics through experimentation."""
    discovered = []
    moves = ['up', 'down', 'left', 'right']
    
    # Observe initial state
    board = world.observe()
    
    # Try some moves and observe changes
    for i in range(min(50, task.get('time_limit_moves', 100))):
        direction = random.choice(moves)
        board_before = world.observe()
        board_after = world.move(direction)
        diffs = world.get_board_diff(board_before, board_after)
        
        # A real agent would analyze diffs and form hypotheses here
        # This is just a stub
        pass
    
    return {
        'completed': len(discovered) >= 10,
        'discovered_mechanics': discovered,
        'steps_taken': world.step_count(),
    }


def solve_navigate(world, task):
    """Level 2: Navigate to target position."""
    target = task.get('target_position', [1, 1])
    
    # Stub: a real agent would plan a path here
    for i in range(task.get('time_limit_moves', 50)):
        world.move(random.choice(['up', 'down', 'left', 'right']))
    
    return {
        'completed': False,  # Replace with actual check
        'steps_taken': world.step_count(),
    }


def solve_deliver(world, task):
    """Level 3: Push mail to house."""
    # Stub: a real agent would plan a push path
    for i in range(task.get('time_limit_moves', 100)):
        world.move(random.choice(['up', 'down', 'left', 'right']))
    
    return {
        'completed': False,
        'steps_taken': world.step_count(),
    }


def solve_optimize(world, task):
    """Level 4: Optimize delivery path."""
    return solve_deliver(world, task)


def solve_counterfactual(world, task):
    """Level 5: Use save-file editing creatively."""
    # Stub: a real agent would read and edit the state file
    state = world.read_state()
    
    # Example: teleport mail next to house (not implemented)
    
    return {
        'completed': False,
        'creativity_score': 0.0,
        'steps_taken': world.step_count(),
    }
