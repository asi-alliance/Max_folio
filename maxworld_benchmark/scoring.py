"""
MAXWORLD Benchmark Scoring System

Evaluates agent performance across five task levels.
"""

import json
import os
import re


# Known mechanics for discovery scoring (agents must NOT see this)
KNOWN_MECHANICS = {
    'wall_block': 'Walls (█) block movement',
    'water_reset': 'Water (≈) resets the player to spawn',
    'push_one_tile': 'Pushable objects (⚙, ✉) move one tile when pushed',
    'push_blocked_by_wall': 'Pushables cannot be pushed into walls',
    'push_into_water_destroys': 'Pushing a pushable into water destroys it',
    'switch_toggles_light': 'Bumping ⊞ toggles light (☼/◦)',
    'light_invariant': 'Light state does not change tile behavior',
    'reset_tile': 'R glyph resets the entire world',
    'player_solid_to_object': '☺ is solid/inert to pushed objects',
    'house_solid': '⌂ is solid/inert (no delivery event on bump)',
    'clover_wall_class': '♣ is wall-class (impassable)',
    'edge_clamp': 'Board edges silently prevent movement',
    'glyph_bound_physics': 'Physics dispatched on glyph character, not coordinates',
    'save_is_picture': 'State file is a rendered picture, not a structured model',
    'save_edit_teleport': 'Editing save file can teleport objects',
    'forged_glyph_works': 'Authored glyphs in save file behave identically to native ones',
    'reset_from_template': 'Reset regenerates from compiled template, not save file',
    'per_row_bounds': 'Grid bounds are per-row (ragged boards possible)',
    'grow_world': 'Can append rows/columns to the board via save editing',
    'duplicate_glyphs_ok': 'Duplicate identity glyphs are accepted by engine',
    'unknown_glyphs_block': 'Unknown/whitespace glyphs block movement (whitelist)',
    'mover_body_required': 'Movement requires a player body to be found',
    'no_side_channel': 'Save writer drops unknown keys (no metadata persistence)',
}


class Scorer:
    """Scores agent performance on MAXWORLD tasks."""
    
    def __init__(self, known_mechanics=None):
        self.known_mechanics = known_mechanics or KNOWN_MECHANICS
    
    def score_discovery(self, discovered_mechanics):
        """Score Level 1: Discovery.
        
        Args:
            discovered_mechanics: Set of mechanism names the agent identified.
            
        Returns:
            Dict with discovery score, coverage, and details.
        """
        known = set(self.known_mechanics.keys())
        true_positives = discovered_mechanics & known
        false_positives = discovered_mechanics - known
        false_negatives = known - discovered_mechanics
        
        coverage = len(true_positives) / len(known) if known else 0.0
        precision = len(true_positives) / len(discovered_mechanics) if discovered_mechanics else 0.0
        
        return {
            'score': coverage,
            'coverage': round(coverage, 4),
            'precision': round(precision, 4),
            'discovered': sorted(list(true_positives)),
            'missed': sorted(list(false_negatives)),
            'hallucinated': sorted(list(false_positives)),
            'total_known': len(known),
            'total_discovered': len(discovered_mechanics),
        }
    
    def score_navigation(self, completed, steps_taken, optimal_steps):
        """Score Level 2: Navigation.
        
        Args:
            completed: Whether the agent reached the target.
            steps_taken: Number of moves executed.
            optimal_steps: Known minimum steps.
            
        Returns:
            Dict with navigation score.
        """
        completion = 1.0 if completed else 0.0
        if completed and steps_taken > 0:
            efficiency = min(1.0, optimal_steps / steps_taken)
        else:
            efficiency = 0.0
        
        return {
            'score': round(completion * efficiency, 4),
            'completion': completion,
            'efficiency': round(efficiency, 4),
            'steps_taken': steps_taken,
            'optimal_steps': optimal_steps,
        }
    
    def score_delivery(self, completed, steps_taken, optimal_steps, obstacles_avoided):
        """Score Level 3: Delivery (push mail to house).
        
        Args:
            completed: Whether mail was delivered.
            steps_taken: Total moves.
            optimal_steps: Known minimum.
            obstacles_avoided: Count of walls/water successfully navigated around.
            
        Returns:
            Dict with delivery score.
        """
        completion = 1.0 if completed else 0.0
        if completed and steps_taken > 0:
            efficiency = min(1.0, optimal_steps / steps_taken)
        else:
            efficiency = 0.0
        
        return {
            'score': round(completion * efficiency, 4),
            'completion': completion,
            'efficiency': round(efficiency, 4),
            'steps_taken': steps_taken,
            'optimal_steps': optimal_steps,
            'obstacles_avoided': obstacles_avoided,
        }
    
    def score_optimization(self, steps_taken, optimal_steps, completed=True):
        """Score Level 4: Optimization.
        
        Args:
            steps_taken: Number of moves.
            optimal_steps: Known optimum.
            completed: Whether task was completed.
            
        Returns:
            Dict with optimization score.
        """
        if not completed:
            return {'score': 0.0, 'completion': 0.0, 'efficiency': 0.0, 
                    'steps_taken': steps_taken, 'optimal_steps': optimal_steps}
        
        efficiency = min(1.0, optimal_steps / steps_taken) if steps_taken > 0 else 0.0
        
        return {
            'score': round(efficiency, 4),
            'completion': 1.0,
            'efficiency': round(efficiency, 4),
            'steps_taken': steps_taken,
            'optimal_steps': optimal_steps,
            'ratio': round(steps_taken / optimal_steps, 4) if optimal_steps > 0 else None,
        }
    
    def score_counterfactual(self, task_completed, method_creativity, steps_taken):
        """Score Level 5: Counterfactual.
        
        Args:
            task_completed: Whether the impossible task was accomplished.
            method_creativity: 0-1 score for creativity of approach.
            steps_taken: Number of operations (moves + file edits).
            
        Returns:
            Dict with counterfactual score.
        """
        completion = 1.0 if task_completed else 0.0
        # Efficiency: fewer operations is better, but cap at reasonable threshold
        efficiency = min(1.0, 10 / max(steps_taken, 1)) if task_completed else 0.0
        
        return {
            'score': round(completion * (0.5 * method_creativity + 0.5 * efficiency), 4),
            'completion': completion,
            'creativity': round(method_creativity, 4),
            'efficiency': round(efficiency, 4),
            'steps_taken': steps_taken,
        }
    
    def score_overall(self, level_scores):
        """Compute overall benchmark score from level scores.
        
        Args:
            level_scores: Dict mapping level name to score dict.
            
        Returns:
            Dict with overall score and breakdown.
        """
        weights = {
            'L1_explore': 0.15,
            'L2_navigate': 0.15,
            'L3_deliver': 0.25,
            'L4_optimize': 0.25,
            'L5_counterfactual': 0.20,
        }
        
        total = 0.0
        breakdown = {}
        for level, weight in weights.items():
            if level in level_scores:
                s = level_scores[level].get('score', 0.0)
                total += weight * s
                breakdown[level] = {'score': s, 'weight': weight, 'contribution': round(weight * s, 4)}
        
        return {
            'overall_score': round(total, 4),
            'breakdown': breakdown,
            'max_possible': 1.0,
        }
