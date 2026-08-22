#!/usr/bin/env python3
"""
MAXWORLD Benchmark - Main Evaluation Harness

Usage:
    python3 benchmark.py --agent your_agent.py --level 1
    python3 benchmark.py --agent your_agent.py --all
    python3 benchmark.py --list
"""

import argparse
import json
import os
import sys
import time
import importlib.util
import subprocess

from wrapper import MaxWorld
from scoring import Scorer, KNOWN_MECHANICS


TASK_FILES = {
    1: 'tasks/L1_explore.json',
    2: 'tasks/L2_navigate.json',
    3: 'tasks/L3_deliver.json',
    4: 'tasks/L4_optimize.json',
    5: 'tasks/L5_counterfactual.json',
}


def load_task(level):
    path = os.path.join(os.path.dirname(__file__), TASK_FILES[level])
    with open(path) as f:
        return json.load(f)


def run_agent(agent_path, world, task, level):
    """Run the agent on a task. The agent module must expose a `solve(world, task)` function."""
    spec = importlib.util.spec_from_file_location('agent', agent_path)
    agent_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(agent_mod)
    
    if not hasattr(agent_mod, 'solve'):
        raise ValueError(f"Agent {agent_path} must define a `solve(world, task)` function.")
    
    return agent_mod.solve(world, task)


def evaluate_level_1(world, scorer, result):
    """Evaluate Level 1: Discovery."""
    discovered = set(result.get('discovered_mechanics', []))
    return scorer.score_discovery(discovered)


def evaluate_level_2(world, scorer, result):
    """Evaluate Level 2: Navigation."""
    completed = result.get('completed', False)
    steps = result.get('steps_taken', world.step_count())
    optimal = result.get('optimal_steps', 14)
    return scorer.score_navigation(completed, steps, optimal)


def evaluate_level_3(world, scorer, result):
    """Evaluate Level 3: Delivery."""
    completed = result.get('completed', False)
    steps = result.get('steps_taken', world.step_count())
    optimal = result.get('optimal_steps', 30)
    obstacles = result.get('obstacles_avoided', 0)
    return scorer.score_delivery(completed, steps, optimal, obstacles)


def evaluate_level_4(world, scorer, result):
    """Evaluate Level 4: Optimization."""
    completed = result.get('completed', False)
    steps = result.get('steps_taken', world.step_count())
    optimal = result.get('optimal_steps', 22)
    return scorer.score_optimization(steps, optimal, completed)


def evaluate_level_5(world, scorer, result):
    """Evaluate Level 5: Counterfactual."""
    completed = result.get('completed', False)
    creativity = result.get('creativity_score', 0.5)
    steps = result.get('steps_taken', world.step_count())
    return scorer.score_counterfactual(completed, creativity, steps)


EVALUATORS = {
    1: evaluate_level_1,
    2: evaluate_level_2,
    3: evaluate_level_3,
    4: evaluate_level_4,
    5: evaluate_level_5,
}


def run_benchmark(agent_path, levels, binary_path='./maxworld', work_dir=None):
    """Run the benchmark for the given levels."""
    scorer = Scorer()
    results = {}
    
    for level in levels:
        task = load_task(level)
        print(f"\n{'='*60}")
        print(f"Level {level}: {task['name']}")
        print(f"{'='*60}")
        print(f"  {task['description'][:100]}...")
        
        world = MaxWorld(binary_path=binary_path, work_dir=work_dir)
        world.reset()
        
        start_time = time.time()
        try:
            result = run_agent(agent_path, world, task, level)
            elapsed = time.time() - start_time
            print(f"  Agent completed in {elapsed:.1f}s, {world.step_count()} steps")
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"  Agent FAILED: {e}")
            result = {'completed': False, 'steps_taken': world.step_count()}
        
        score = EVALUATORS[level](world, scorer, result)
        results[f'L{level}_{task[\"name\"].lower()}'] = score
        print(f"  Score: {score.get('score', 0.0):.4f}")
    
    overall = scorer.score_overall(results)
    print(f"\n{'='*60}")
    print(f"Overall Score: {overall['overall_score']:.4f} / 1.0")
    print(f"{'='*60}")
    for level, info in overall['breakdown'].items():
        print(f"  {level}: {info['score']:.4f} (weight={info['weight']}, contrib={info['contribution']})")
    
    return {'levels': results, 'overall': overall}


def main():
    parser = argparse.ArgumentParser(description='MAXWORLD Benchmark for AI Agents')
    parser.add_argument('--agent', type=str, help='Path to agent Python file')
    parser.add_argument('--level', type=int, choices=[1,2,3,4,5], help='Single level to run')
    parser.add_argument('--all', action='store_true', help='Run all levels')
    parser.add_argument('--list', action='store_true', help='List available levels')
    parser.add_argument('--binary', type=str, default='./maxworld', help='Path to maxworld binary')
    parser.add_argument('--work-dir', type=str, default=None, help='Working directory')
    parser.add_argument('--output', type=str, default=None, help='Save results to JSON file')
    args = parser.parse_args()
    
    if args.list:
        print("Available levels:")
        for level in range(1, 6):
            task = load_task(level)
            print(f"  Level {level}: {task['name']} - {task['description'][:80]}...")
        return
    
    if not args.agent:
        parser.error('--agent is required (unless using --list)')
    
    levels = [args.level] if args.level else [1,2,3,4,5] if args.all else [1]
    
    results = run_benchmark(args.agent, levels, args.binary, args.work_dir)
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to {args.output}")


if __name__ == '__main__':
    main()
