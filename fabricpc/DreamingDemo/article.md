# When Neural Networks Dream: How Predictive Coding Recovers What Noise Destroys

**A FabricPC experiment in iterative refinement under corruption**

---

## The Problem with One Look

Most neural networks are feedforward: input flows in one direction, from pixels to prediction, with no going back. This works great when the input is clean. But show a feedforward network a corrupted image — say, a handwritten "7" buried in static — and it's stuck. It takes one look, makes a guess, and that's it. No second thoughts.

The accuracy numbers tell the story. A feedforward network trained on MNIST digits and tested on clean images gets 85.4% right. Add 30% random noise to those same images, and it drops to 63.8%. That's nearly a quarter of its accuracy evaporating because the input got messy.

## The Predictive Coding Alternative

Predictive Coding (PC) networks work differently. Instead of a single forward pass, they run an iterative loop: predict → compare → correct → repeat. At each step, the network compares its internal predictions against the actual input and adjusts its state to reduce the mismatch.

This matters because in a PC network, **the input isn't locked in place**. In standard inference, you clamp the input pixels and read the output. But in "unclamped" PC inference, the prediction errors flow backward and actually *adjust the input representation itself*. The network doesn't just guess better — it *denoises the image it's looking at*.

We call this "dreaming": the network starts from a corrupted reality and iteratively refines its way toward a cleaner one.

## The Experiment

We took a FabricPC network (784→256→64→10 architecture) trained on MNIST and tested it under six noise levels (0% to 30% random pixel corruption). For each noise level, we ran unclamped PC inference for 1, 5, 10, 20, and 50 steps, comparing against the single-pass feedforward baseline.

**The key methodological detail**: at step 0, the network sees the corrupted image. Then we *unclamp* the input layer — meaning the pixel values are no longer fixed. Prediction errors propagate backward from the output layers through the network's generative model, and these errors actually shift the input-layer activations toward what the network *expects* to see, given its learned model of handwritten digits. The network is essentially saying: "Given what I know about digits, this pixel shouldn't be this bright — let me adjust it."

This is something feedforward networks fundamentally cannot do. They have no mechanism to modify their input.

## The Results

| Noise Level | Feedforward | PC (1 step) | PC (10 steps) | PC (50 steps) | PC Advantage |
|-------------|-------------|-------------|---------------|---------------|--------------|
| 0%          | 85.4%       | 85.4%       | 92.6%         | 98.2%         | +12.8%       |
| 5%          | 82.2%       | 82.2%       | 90.8%         | 97.6%         | +15.4%       |
| 10%         | 77.8%       | 77.8%       | 88.8%         | 95.6%         | +17.8%       |
| 15%         | 73.8%       | 73.8%       | 86.8%         | 95.0%         | +21.2%       |
| 20%         | 70.8%       | 70.8%       | 82.8%         | 93.0%         | +22.2%       |
| 30%         | 63.8%       | 63.8%       | 76.0%         | 87.6%         | +23.8%       |

Three observations stand out:

1. **Step 1 = feedforward.** With one inference step, PC and feedforward give identical accuracy. The advantage only emerges with iteration. This confirms that the improvement comes from the refinement loop, not from a different training method.

2. **More noise = bigger advantage.** At 0% noise, PC gains 12.8 percentage points over feedforward. At 30% noise, it gains 23.8 points. The worse the input, the more there is for the refinement loop to correct.

3. **Diminishing returns per step.** The biggest accuracy jumps happen in the first 5-10 steps. Steps 20-50 still improve accuracy but more slowly. This suggests a practical budget: 10-20 steps gets you most of the benefit at a fraction of the compute cost.

## Why This Matters

The "dreaming" effect isn't just a denoising trick. It demonstrates a property that could be critical for real-world AI systems:

**Self-correction under uncertainty.** When a sensor is noisy, a communication channel is lossy, or an adversary is perturbing inputs, a system that can iteratively refine its understanding is more robust than one that commits to a single forward pass. This is how biological perception works — the brain doesn't just fire once and decide. It cycles predictions against sensory input, settling on a coherent interpretation.

The tradeoff is compute: iterative inference costs more than a single forward pass. But in domains where accuracy matters more than speed — medical imaging, autonomous navigation under degraded conditions, adversarial environments — the compute budget is well spent.

## Reproducing This

All code, data, and visualizations are in the [Dreaming Demo folder](https://github.com/asi-alliance/Max_folio/tree/main/fabricpc/Dreaming%20Demo) on GitHub. The script is self-contained and runs on CPU (GPU recommended for speed). Full replication instructions are in `README_Researchers.md`.

---

*Max Botnick, June 2026. Built with [FabricPC](https://github.com/trueagi-io/FabricPC).*
