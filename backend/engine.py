"""
Linguistic Resonator: Semantic Search via Phase Synchronization
---------------------------------------------------------------
Author: Douglas Henrique Machado Fulber (via Antigravity AI)
Date: 2025-12-27

Concept:
In standard AI, we find related words using Vector Math (Cosine Similarity).
In IoC (Internet of Consciousness), we find related words using PHYSICS (Resonance).

Mechanism:
1. Each word is an Oscillator.
2. Semantic relationship = Coupling Strength (K).
3. Query = Forcing a specific frequency on one word.
4. Result = Which other words synchronize?

Scenario:
Vocabulary: ["King", "Queen", "Man", "Woman", "Apple", "Fruit", "Car", "Engine"]
We activate "King". "Queen" should resonate. "Apple" should remain phase-locked to specific background or noise.
"""

import numpy as np
import matplotlib.pyplot as plt
import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Word Vocabulary
words = ["King", "Queen", "Man", "Woman", "Apple", "Fruit", "Car", "Engine"]
n_words = len(words)

# Semantic Coupling Matrix (K_ij)
# Higher value = Stronger semantic link
K_matrix = np.zeros((n_words, n_words))

# Define relationships manually for PoC (In v1.0 this is learned)
associations = [
    ("King", "Queen", 5.0),
    ("King", "Man", 3.0),
    ("Queen", "Woman", 3.0),
    ("Man", "Woman", 2.0),
    ("Apple", "Fruit", 5.0),
    ("Car", "Engine", 5.0),
    ("King", "Car", 0.0), # No relation
    ("Apple", "Engine", 0.0) # No relation
]

idx_map = {w: i for i, w in enumerate(words)}

print("[INIT] Building Semantic Lattice...")
for w1, w2, k in associations:
    i, j = idx_map[w1], idx_map[w2]
    K_matrix[i, j] = k
    K_matrix[j, i] = k # Symmetric

def kuramoto_step(phases, omega, dt=0.01):
    """
    d(theta_i)/dt = omega_i + sum( K_ij * sin(theta_j - theta_i) )
    """
    n = len(phases)
    d_theta = np.zeros(n)
    
    for i in range(n):
        interaction = 0.0
        for j in range(n):
            if K_matrix[i, j] > 0:
                interaction += K_matrix[i, j] * np.sin(phases[j] - phases[i])
        
        d_theta[i] = omega[i] + interaction
        
    return phases + d_theta * dt

def run_linguistic_resonance(target_word="King", steps=1000):
    print(f"[QUERY] Activating concept: '{target_word}'")
    
    # Initialize phases random
    phases = np.random.uniform(0, 2*np.pi, n_words)
    
    # Natural Frequencies
    # Background words vibrate at random frequencies
    omega = np.random.normal(1.0, 0.1, n_words)
    
    # The Target Word is "Forced" to a specific frequency (The "Input")
    target_idx = idx_map[target_word]
    omega[target_idx] = 1.0 # Reference frequency
    
    # History for plotting
    history = np.zeros((steps, n_words))
    
    # Run Simulation
    for t in range(steps):
        phases = kuramoto_step(phases, omega)
        history[t] = phases
        
    # Calculate Synchronization Level (Order Parameter R) with Target
    # R_j = | < e^(i(theta_j - theta_target)) > | (time average)
    
    print("[ANALYSIS] Measuring Resonance with Target...")
    resonances = {}
    target_phase_hist = history[:, target_idx]
    
    for i, word in enumerate(words):
        if i == target_idx: continue
        
        # Simple Phase Difference metric (cos distance averaged)
        # 1.0 = Perfectly Synced
        # 0.0 = Uncorrelated
        phase_diff = np.cos(history[:, i] - target_phase_hist)
        sync_score = np.mean(phase_diff[-200:]) # Last 200 steps
        resonances[word] = sync_score

    return history, resonances

def visualize_resonance(history, resonances, target_word):
    # Plot 1: Phase Evolution
    plt.figure(figsize=(14, 6))
    
    # Plot phases (wrapped to 0-2pi visually or just raw)
    # Raw is better to show locking
    for i, word in enumerate(words):
        alpha = 1.0 if word == target_word else 0.5
        width = 3.0 if word == target_word else 1.5
        ls = '-'
        
        # Color based on final resonance?
        if word == target_word: color = 'black'
        elif resonances.get(word, 0) > 0.8: color = 'green' # Resonating
        elif resonances.get(word, 0) > 0.5: color = 'blue'  # Weak
        else: color = 'gray' # Noise
        
        plt.plot(history[:, i], label=word, color=color, alpha=alpha, linewidth=width, linestyle=ls)
        
    plt.title(f"Linguistic Resonance: Querying '{target_word}'")
    plt.xlabel("Time")
    plt.ylabel("Phase (Theta)")
    plt.legend(loc='upper left')
    
    out_path = os.path.join(OUTPUT_DIR, 'linguistic_resonance_plot.png')
    plt.savefig(out_path)
    print(f"[RESULT] Plot saved to: {out_path}")
    
    # Print Results
    print("\n--- Semantic Resonance Results ---")
    sorted_res = sorted(resonances.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_res:
        bar = "#" * int(score * 20)
        print(f"{word.ljust(10)}: {score:.4f} {bar}")

if __name__ == "__main__":
    hist, res = run_linguistic_resonance("King")
    visualize_resonance(hist, res, "King")
