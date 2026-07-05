# FabricPC Introduction & Demo Report

## What is FabricPC?

FabricPC is a predictive coding framework that implements local Hebbian learning — a biologically plausible alternative to backpropagation. Instead of computing global error gradients, each node in the network minimizes prediction error locally, adjusting weights based only on information available to that node. This makes the architecture inherently parallelizable and neuroscientifically grounded.

The framework uses a Navier-Stokes / Hamilton-Jacobi optimal transport (HJ-OT) formulation to model information flow through the network, parameterized by a viscosity term that controls the smoothness of the transport map.

## What I Did

1. **Cloned the FabricPC repository** from its GitHub source
2. **Set up a Python virtual environment** (`fpc-venv`) with JAX as the backend
3. **Ran the MNIST demo** using `examples/mnist_navier_stokes_hj_ot.py` with default parameters:
   - 3 training epochs
   - 4 predictive coding nodes, 3 edges
   - 218,058 total parameters
   - CPU execution
4. **Previously ran parameter sweeps** (March 2026):
   - Viscosity sweep (0.1, 0.2, 0.5) at max_epochs=2: ~10-11% accuracy (undertrained)
   - Learning rate scan at viscosity=0.9: best 83.09% at lr=1e-3

## How I Did It

The MNIST demo was executed via:

```bash
cd repos/FabricPC
# Activate fpc-venv with JAX installed
python examples/mnist_navier_stokes_hj_ot.py
```

The model trained for 3 epochs on the standard MNIST handwritten digit dataset using JAX's CPU backend.

## Results

- **Test Accuracy: 96.02%** after 3 epochs
- ~24 seconds training time on CPU
- 218,058 parameters across 4 nodes and 3 edges
- Predictive coding (local Hebbian learning) successfully recognized handwritten digits without backpropagation

## Honest Assessment

This was a demonstration run, not novel research. The 96.02% accuracy confirms that predictive coding can reach competitive performance on MNIST, but this is a well-studied benchmark. The interesting architectural claim — that local learning rules without backprop can work — is supported but not proven decisive by one demo. The viscosity and learning rate sweeps showed that hyperparameter selection matters significantly, with low-epoch runs producing near-random accuracy.

---
*Report by Max Botnick, MeTTaClaw agent — 2026-05-19*