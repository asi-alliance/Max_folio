#!/usr/bin/env python3
"""
MAXWORLD Benchmark Setup Script

Prepares a clean working directory for benchmarking.
"""

import os
import sys
import shutil
import json


def setup(work_dir='./maxworld_run', binary_path='./maxworld'):
    """Set up a clean MAXWORLD working directory."""
    os.makedirs(work_dir, exist_ok=True)
    
    # Copy binary
    if os.path.exists(binary_path):
        dest = os.path.join(work_dir, 'maxworld')
        shutil.copy2(binary_path, dest)
        os.chmod(dest, 0o755)
        print(f'  Copied binary to {dest}')
    else:
        print(f'  WARNING: Binary not found at {binary_path}')
    
    # Copy state file
    state_src = '.myworld_state.json'
    if os.path.exists(state_src):
        shutil.copy2(state_src, os.path.join(work_dir, '.myworld_state.json'))
        print(f'  Copied state file')
    else:
        print(f'  WARNING: State file not found at {state_src}')
    
    # Copy wrapper and scoring
    bench_dir = os.path.dirname(os.path.abspath(__file__))
    for f in ['wrapper.py', 'scoring.py', 'benchmark.py', 'example_agent.py']:
        src = os.path.join(bench_dir, f)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(work_dir, f))
    
    # Copy tasks
    tasks_dir = os.path.join(work_dir, 'tasks')
    os.makedirs(tasks_dir, exist_ok=True)
    src_tasks = os.path.join(bench_dir, 'tasks')
    if os.path.exists(src_tasks):
        for f in os.listdir(src_tasks):
            shutil.copy2(os.path.join(src_tasks, f), os.path.join(tasks_dir, f))
    
    print(f'\nSetup complete! Working directory: {work_dir}')
    print(f'To run: cd {work_dir} && python3 benchmark.py --agent example_agent.py --all')


if __name__ == '__main__':
    work_dir = sys.argv[1] if len(sys.argv) > 1 else './maxworld_run'
    binary = sys.argv[2] if len(sys.argv) > 2 else './maxworld'
    setup(work_dir, binary)
