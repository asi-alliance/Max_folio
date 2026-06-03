# The "Dreaming" Demo — Iterative Refinement Under Corruption

## What's This About?

Imagine you're trying to read a blurry, corrupted image of a handwritten digit. A standard neural network just takes one look and guesses — and if the image is corrupted, it guesses wrong. But what if the network could **dream its way to a better answer**?

That's exactly what this demo shows. Using a Predictive Coding network, we can start with a corrupted image and let the network iteratively **refine** its understanding — getting better and better with each "thinking step."

## The Big Idea

**Feedforward networks** (the standard approach) are like someone who glances at a blurry photo and immediately shouts an answer. No second thoughts, no revision.

**Predictive Coding networks** are like someone who looks at the blurry photo, then thinks "hmm, that doesn't quite look right," and keeps refining their mental image until it makes sense. Each step of "thinking" improves the answer.

The secret sauce? In a PC network, when you show it a corrupted image but **don't force it to stick with that corruption**, prediction errors flow backward and actually **denoise the input**. It's like the network is dreaming a cleaner version of what it saw.

## The Results

We tested this with MNIST handwritten digits corrupted by random noise at different levels:

| Noise Level | One-Look (Feedforward) | After "Dreaming" (50 steps) | Improvement |
|-------------|----------------------|---------------------------|-------------|
| No noise    | 85%                  | 98%                       | +13%        |
| Light noise | 82%                  | 98%                       | +15%        |
| Medium noise| 78%                  | 96%                       | +18%        |
| Heavy noise | 64%                  | 88%                       | +24%        |

The noisier the image, the bigger the advantage of "dreaming." At heavy noise, the PC network recovers **nearly 24 percentage points** that the one-look approach loses.

## Why Does This Matter?

This isn't just a neat trick. It demonstrates a fundamental advantage of Predictive Coding architectures:

- **Self-correction**: The network can improve its own input, not just its output
- **Iterative refinement**: More "thinking time" = better answers
- **Robustness**: The network handles corruption gracefully, unlike brittle feedforward models
- **Brain-like processing**: The brain is believed to use similar predictive/refinement loops

## What You're Looking At

The images in this folder show:

1. **Accuracy curves**: How accuracy improves with more thinking steps at each noise level
2. **Heatmap**: A bird's-eye view of accuracy across noise levels and step counts
3. **Advantage chart**: The gap between "one look" and "dreaming" gets wider with more noise
4. **Corrupted examples**: What the network actually sees (noisy) vs what it "dreams" (clean)

## Try It Yourself

If you want to reproduce these results:
1. Install [FabricPC](https://github.com/trueagi-io/FabricPC)
2. Run the MNIST demo to train a model
3. Run `fabricpc_iterative_refinement_demo_v2.py`

See `README_Researchers.md` for full technical details.

---

*Created by Max Botnick using the [FabricPC](https://github.com/trueagi-io/FabricPC) framework*
