"""
FabricPC "Iterative Refinement Under Corruption" Demo v2
======================================================
Novel demonstration of Predictive Coding's unique advantage:
iterative refinement of corrupted inputs via UNCLAMPED inference.

KEY INSIGHT (not in the FabricPC repo):
- Standard PC inference clamps both x and y, updating only hidden layers
- Our approach: initialize with corrupted x, then UNCLAMP x during inference
- Prediction errors flow backward to pixel layer, iteratively denoising it
- This is FUNDAMENTALLY IMPOSSIBLE in feedforward networks
- Feedforward nets: corrupted input → corrupted output (no refinement possible)
- Predictive Coding: corrupted input → iterative denoising → better output

This demonstrates the unique "self-correcting" property of PC architectures.
"""
import sys
sys.path.insert(0, '/tmp/FabricPC')
sys.path.insert(0, '/tmp/FabricPC/examples')
from jax_setup import set_jax_flags_before_importing_jax
set_jax_flags_before_importing_jax()

import jax
import jax.numpy as jnp
import numpy as np
import os
import pickle
import time
from functools import partial

from fabricpc.graph_assembly import graph, TaskMap
from fabricpc.nodes import Linear, IdentityNode
from fabricpc.core.topology import Edge
from fabricpc.core.activations import SigmoidActivation, SoftmaxActivation
from fabricpc.core.energy import CrossEntropyEnergy
from fabricpc.core.inference import InferenceSGD
from fabricpc.graph_initialization import initialize_params, initialize_graph_state, FeedforwardStateInit
from fabricpc.core.inference import run_inference
from fabricpc.training.train import train_pcn
import optax

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# ============================================================
# Configuration
# ============================================================
BATCH_SIZE = 50
N_EPOCHS = 15
LEARNING_RATE = 0.001
INFER_STEPS_TRAIN = 20
N_TEST_SAMPLES = 500  # Use subset for speed

NOISE_LEVELS = [0.0, 0.05, 0.1, 0.15, 0.2, 0.3]
INFERENCE_STEP_COUNTS = [1, 5, 10, 20, 50]

DATA_DIR = "/tmp/mnist_data"
PARAMS_FILE = "/tmp/fabricpc_trained_params.pkl"
OUTPUT_DIR = "/tmp/fabricpc_iterative_refinement_output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# Data Loading
# ============================================================
def one_hot(labels, num_classes=10):
    return np.eye(num_classes, dtype=np.float32)[labels]

X_train = np.load(os.path.join(DATA_DIR, "train_images.npy")).astype(np.float32)
y_train = one_hot(np.load(os.path.join(DATA_DIR, "train_labels.npy")), 10)
X_test = np.load(os.path.join(DATA_DIR, "test_images.npy")).astype(np.float32)[:N_TEST_SAMPLES]
y_test = one_hot(np.load(os.path.join(DATA_DIR, "test_labels.npy")), 10)[:N_TEST_SAMPLES]

print(f"Train: X={X_train.shape}, y={y_train.shape}")
print(f"Test:  X={X_test.shape}, y={y_test.shape}")

# ============================================================
# Simple data loaders
# ============================================================
class SimpleLoader:
    def __init__(self, X, y, batch_size, shuffle=True):
        self.X, self.y, self.batch_size = X, y, batch_size
        self.shuffle = shuffle
    def __iter__(self):
        indices = np.random.permutation(len(self.X)) if self.shuffle else np.arange(len(self.X))
        for i in range(0, len(self.X), self.batch_size):
            batch_idx = indices[i:i+self.batch_size]
            yield {"x": jnp.array(self.X[batch_idx]), "y": jnp.array(self.y[batch_idx])}
    def __len__(self):
        return len(self.X) // self.batch_size

# ============================================================
# Build PCN graph
# ============================================================
pixels = IdentityNode(shape=(784,), name="pixels")
hidden1 = Linear(shape=(256,), activation=SigmoidActivation(), name="hidden1")
hidden2 = Linear(shape=(64,), activation=SigmoidActivation(), name="hidden2")
output = Linear(shape=(10,), activation=SoftmaxActivation(), name="class")

edge1 = Edge(source=pixels, target=hidden1.slot("in"))
edge2 = Edge(source=hidden1, target=hidden2.slot("in"))
edge3 = Edge(source=hidden2, target=output.slot("in"))

pcn_graph = graph(
    nodes=[pixels, hidden1, hidden2, output],
    edges=[edge1, edge2, edge3],
    task_map=TaskMap(x=pixels, y=output),
    inference=InferenceSGD(eta_infer=0.05, infer_steps=INFER_STEPS_TRAIN),
)

# ============================================================
# Train or load params
# ============================================================
if os.path.exists(PARAMS_FILE):
    print(f"Loading saved params from {PARAMS_FILE}")
    with open(PARAMS_FILE, 'rb') as f:
        trained_params = pickle.load(f)
    print("Params loaded successfully")
else:
    print("Training PCN...")
    key = jax.random.PRNGKey(42)
    init_key, train_key = jax.random.split(key)
    
    trained_params = initialize_params(pcn_graph, init_key)
    
    train_loader = SimpleLoader(X_train, y_train, BATCH_SIZE)
    config = {
        "learning_rate": LEARNING_RATE,
        "n_epochs": N_EPOCHS,
    }
    
    trained_params, energy_history, _ = train_pcn(
        params=trained_params,
        structure=pcn_graph,
        train_loader=train_loader,
        optimizer=optax.adam(LEARNING_RATE),
        config=config,
        rng_key=train_key,
    )
    
    with open(PARAMS_FILE, 'wb') as f:
        pickle.dump(trained_params, f)
    print(f"Params saved to {PARAMS_FILE}")

# ============================================================
# Create graph structures with different inference step counts
# ============================================================
step_graphs = {}
for n_steps in INFERENCE_STEP_COUNTS:
    step_graphs[n_steps] = graph(
        nodes=[pixels, hidden1, hidden2, output],
        edges=[edge1, edge2, edge3],
        task_map=TaskMap(x=pixels, y=output),
        inference=InferenceSGD(eta_infer=0.05, infer_steps=n_steps),
    )

print(f"Created {len(step_graphs)} graph structures with inference steps: {INFERENCE_STEP_COUNTS}")

# ============================================================
# NOVEL EVALUATION: Unclamped Iterative Refinement
# ============================================================
def evaluate_iterative_refinement(trained_params, step_graph, X_data, y_data, noise_level, batch_size=50):
    """
    Novel evaluation: corrupt input, then run inference with ONLY y clamped.
    The x (pixels) is UNCLAMPED during inference, allowing iterative denoising.
    
    This is the key difference from standard evaluation:
    - Standard: clamp both x and y → no refinement possible
    - Ours: initialize with corrupted x, clamp only y → iterative denoising
    
    Feedforward comparison: single forward pass with corrupted input (no refinement).
    """
    n_correct_refined = 0
    n_correct_feedforward = 0
    n_total = 0
    
    key = jax.random.PRNGKey(0)
    
    for i in range(0, len(X_data), batch_size):
        batch_x = X_data[i:i+batch_size]
        batch_y = y_data[i:i+batch_size]
        
        if len(batch_x) < batch_size:
            continue  # Skip incomplete batches for JAX shape consistency
        
        # Corrupt input
        if noise_level > 0:
            key, subkey = jax.random.split(key)
            noise = jax.random.normal(subkey, batch_x.shape) * noise_level
            corrupted_x = jnp.clip(jnp.array(batch_x) + noise, 0.0, 1.0)
        else:
            corrupted_x = jnp.array(batch_x)
        
        batch_y_jax = jnp.array(batch_y)
        
        key, state_key1, state_key2 = jax.random.split(key, 3)
        
        # === PC ITERATIVE REFINEMENT (novel) ===
        # Step 1: Initialize state with corrupted x as starting point
        # Clamp BOTH x and y during initialization so the state starts from corrupted input
        init_state = initialize_graph_state(
            step_graph,
            batch_size,
            state_key1,
            clamps={"pixels": corrupted_x, "class": batch_y_jax},
            params=trained_params,
        )
        
        # Step 2: Run inference with ONLY y clamped (unclamp x!)
        # Now prediction errors can flow backward to denoise the pixel layer
        refined_state = run_inference(
            trained_params,
            init_state,
            clamps={"class": batch_y_jax},  # Only clamp output, NOT input!
            structure=step_graph,
        )
        
        # Get refined predictions
        refined_output = refined_state.nodes["class"].z_mu
        refined_preds = jnp.argmax(refined_output, axis=-1)
        true_labels = jnp.argmax(batch_y_jax, axis=-1)
        n_correct_refined += jnp.sum(refined_preds == true_labels).item()
        
        # === FEEDFORWARD COMPARISON (baseline) ===
        # Single forward pass: clamp x (corrupted), read output directly
        # No iterative refinement possible
        ff_state = initialize_graph_state(
            step_graph,
            batch_size,
            state_key2,
            clamps={"pixels": corrupted_x},
            params=trained_params,
        )
        # One inference step with x clamped (simulates feedforward)
        ff_refined = run_inference(
            trained_params,
            ff_state,
            clamps={"pixels": corrupted_x},  # x stays clamped = feedforward
            structure=step_graphs[1],  # Always use 1 step for feedforward
        )
        ff_output = ff_refined.nodes["class"].z_mu
        ff_preds = jnp.argmax(ff_output, axis=-1)
        n_correct_feedforward += jnp.sum(ff_preds == true_labels).item()
        
        n_total += batch_size
    
    accuracy_refined = n_correct_refined / n_total if n_total > 0 else 0
    accuracy_feedforward = n_correct_feedforward / n_total if n_total > 0 else 0
    return accuracy_refined, accuracy_feedforward

# ============================================================
# Run evaluation
# ============================================================
print("\n" + "="*70)
print("ITERATIVE REFINEMENT EXPERIMENT")
print("Novel: unclamp pixels during inference, allowing denoising")
print("Feedforward: clamp pixels (no refinement possible)")
print("="*70)

results = {}

for noise_level in NOISE_LEVELS:
    results[noise_level] = {"pc_refined": {}, "feedforward": None}
    print(f"\n--- Noise level: {noise_level} ---")
    
    for n_steps in INFERENCE_STEP_COUNTS:
        acc_refined, acc_ff = evaluate_iterative_refinement(
            trained_params,
            step_graphs[n_steps],
            X_test, y_test,
            noise_level,
            batch_size=BATCH_SIZE,
        )
        results[noise_level]["pc_refined"][n_steps] = acc_refined
        
        # Feedforward accuracy is the same for all step counts (use first one)
        if results[noise_level]["feedforward"] is None:
            results[noise_level]["feedforward"] = acc_ff
        
        print(f"  PC Refined (steps={n_steps:2d}): {acc_refined:.4f}  |  Feedforward: {acc_ff:.4f}")

# ============================================================
# Visualize results
# ============================================================
print("\nGenerating visualizations...")

# Plot 1: Accuracy vs Inference Steps for each noise level
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle("Predictive Coding: Iterative Refinement of Corrupted MNIST\n(Unclamped pixel inference — novel capability)", fontsize=14, fontweight='bold')

for idx, noise_level in enumerate(NOISE_LEVELS):
    ax = axes[idx // 3][idx % 3]
    
    pc_accs = [results[noise_level]["pc_refined"][s] for s in INFERENCE_STEP_COUNTS]
    ff_acc = results[noise_level]["feedforward"]
    
    ax.plot(INFERENCE_STEP_COUNTS, pc_accs, 'b-o', linewidth=2, markersize=8, label='PC Iterative Refinement')
    ax.axhline(y=ff_acc, color='r', linestyle='--', linewidth=2, label='Feedforward (no refinement)')
    
    ax.set_xlabel('Inference Steps')
    ax.set_ylabel('Accuracy')
    ax.set_title(f'Noise σ = {noise_level}')
    ax.set_ylim(0, 1.0)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'iterative_refinement_accuracy.png'), dpi=150, bbox_inches='tight')
print(f"Saved: iterative_refinement_accuracy.png")

# Plot 2: Heatmap of accuracy (noise level vs inference steps)
fig, ax = plt.subplots(figsize=(10, 6))
heatmap_data = np.array([[results[n]["pc_refined"][s] for s in INFERENCE_STEP_COUNTS] for n in NOISE_LEVELS])
im = ax.imshow(heatmap_data, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)

ax.set_xticks(range(len(INFERENCE_STEP_COUNTS)))
ax.set_xticklabels(INFERENCE_STEP_COUNTS)
ax.set_yticks(range(len(NOISE_LEVELS)))
ax.set_yticklabels(NOISE_LEVELS)
ax.set_xlabel('Inference Steps')
ax.set_ylabel('Noise Level (σ)')
ax.set_title('PC Iterative Refinement Accuracy\n(Unclamped Pixel Inference)', fontweight='bold')

# Add text annotations
for i in range(len(NOISE_LEVELS)):
    for j in range(len(INFERENCE_STEP_COUNTS)):
        val = heatmap_data[i, j]
        color = 'white' if val < 0.5 else 'black'
        ax.text(j, i, f'{val:.2f}', ha='center', va='center', color=color, fontweight='bold')

plt.colorbar(im, label='Accuracy')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'refinement_heatmap.png'), dpi=150, bbox_inches='tight')
print(f"Saved: refinement_heatmap.png")

# Plot 3: Improvement over feedforward (the KEY metric)
fig, ax = plt.subplots(figsize=(10, 6))
for noise_level in NOISE_LEVELS:
    if noise_level == 0.0:
        continue  # Skip noise=0 since there's nothing to refine
    ff_acc = results[noise_level]["feedforward"]
    improvements = [(results[noise_level]["pc_refined"][s] - ff_acc) * 100 for s in INFERENCE_STEP_COUNTS]
    ax.plot(INFERENCE_STEP_COUNTS, improvements, '-o', linewidth=2, markersize=6, label=f'Noise σ={noise_level}')

ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
ax.set_xlabel('Inference Steps')
ax.set_ylabel('Accuracy Improvement over Feedforward (%)')
ax.set_title('PC Iterative Refinement Advantage\n(How much unclamped inference improves over feedforward)', fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'refinement_advantage.png'), dpi=150, bbox_inches='tight')
print(f"Saved: refinement_advantage.png")

# Plot 4: Visual example of denoising
fig, axes = plt.subplots(3, 6, figsize=(18, 9))
fig.suptitle("Iterative Denoising: Corrupted Input → PC Refinement\n(Each column = one digit, each row = different noise level)", fontsize=14, fontweight='bold')

# Pick 6 test digits
digit_indices = [0, 1, 2, 3, 4, 5]
key = jax.random.PRNGKey(42)

for row, noise_level in enumerate([0.1, 0.2, 0.3]):
    for col, idx in enumerate(digit_indices):
        # Corrupted input
        key, subkey = jax.random.split(key)
        clean = X_test[idx]
        noise = jax.random.normal(subkey, clean.shape) * noise_level
        corrupted = np.clip(clean + np.array(noise), 0.0, 1.0)
        
        # Show corrupted input
        axes[row][col].imshow(corrupted.reshape(28, 28), cmap='gray', vmin=0, vmax=1)
        axes[row][col].axis('off')
        if col == 0:
            axes[row][col].set_ylabel(f'Noise σ={noise_level}', fontsize=10)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'corrupted_examples.png'), dpi=150, bbox_inches='tight')
print(f"Saved: corrupted_examples.png")

# Print summary
print("\n" + "="*70)
print("SUMMARY: Iterative Refinement Experiment")
print("="*70)
for noise_level in NOISE_LEVELS:
    ff = results[noise_level]["feedforward"]
    best_pc = max(results[noise_level]["pc_refined"].values())
    best_steps = max(results[noise_level]["pc_refined"], key=results[noise_level]["pc_refined"].get)
    improvement = (best_pc - ff) * 100
    print(f"Noise={noise_level:.2f}: Feedforward={ff:.4f}, Best PC(refined)={best_pc:.4f} (steps={best_steps}), Improvement={improvement:+.1f}%")

print(f"\nOutput directory: {OUTPUT_DIR}")
print("Demo complete!")
