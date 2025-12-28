"""
BitNet Core: The Semantic Engine of ResonantReader (v3.0)
---------------------------------------------------------
Author: Douglas Henrique Machado Fulber (via Antigravity AI)
Imported from: IoC_Resonant_AI/prototype_bitnet_resonator.py

USAGE IN PRODUCT:
This module provides the `ResonantBitNet` class.
Instead of hardcoding connections like ("King", "Queen"), we will:
1. Convert PDF text into sparse vectors (Embeddings).
2. Feed vectors into `ResonantBitNet.train_hebbian()`.
3. Call `cristallize()` to compress knowledge into 1.58-bit weights.
4. Use `self.J_final` (The Adjacency Matrix) to drive the D3.js Graph.
"""

import numpy as np
import os

class ResonantBitNet:
    def __init__(self, n_neurons):
        self.N = n_neurons
        # Initialize weights as Float first (Plasticity phase)
        self.J = np.zeros((n_neurons, n_neurons))
        self.J_final = None
        
    def train_hebbian(self, patterns):
        """Standard Hebbian Learning: W += x * x.T"""
        print(f"[LEARNING] Absorbing {len(patterns)} patterns...")
        for p in patterns:
            p = p.reshape(-1, 1)
            self.J += p @ p.T
            
        # Remove self-connections
        np.fill_diagonal(self.J, 0)
        
    def cristallize(self):
        """
        The 'BitNet' Step:
        Freeze the liquid analog weights into solid Ternary Weights {-1, 0, 1}.
        This is the 'Adulthood' of the network.
        """
        print("[CRITICAL PHASE] Crystallizing weights to 1.58-bit ({-1, 0, 1})...")
        self.J_ternary = self._quantize_weights(self.J)
        
        # Calculate compression ratio (assuming float32 vs 2-bit storage)
        print(f"   Original Memory: {self.N*self.N*32} bits")
        print(f"   BitNet Memory:   {self.N*self.N*2}  bits (16x Compression)")
        
        # Use ternary weights from now on
        self.J_final = self.J_ternary

    def _quantize_weights(self, W):
        """
        Simulate BitNet 1.58-bit quantization.
        Maps continuous weights to {-1, 0, 1}.
        """
        # BitNet strategy: Scale by average absolute value
        gamma = np.mean(np.abs(W)) + 1e-9
        W_scaled = W / gamma
        
        # Round to nearest integer among {-1, 0, 1}
        W_quant = np.round(W_scaled)
        W_quant = np.clip(W_quant, -1, 1)
        
        return W_quant.astype(np.int8)

    def get_adjacency_matrix(self):
        """Returns the crystallized matrix for the Physics Engine"""
        if self.J_final is None:
            raise ValueError("Network not crystallized yet!")
        return self.J_final

    def recall(self, query, max_steps=10):
        """
        Run resonance dynamics to recover memory.
        s(t+1) = sign( sum( J_ij * s_j ) )
        """
        if self.J_final is None:
             raise ValueError("Network not crystallized yet!")
             
        state = query.copy()
        energy_history = []
        
        for step in range(max_steps):
            # Synchronous update
            h = self.J_final @ state
            new_state = np.sign(h)
            new_state[new_state == 0] = state[new_state == 0]
            
            # Energy Calculation
            E = -0.5 * state.T @ self.J_final @ state
            energy_history.append(E)
            
            diff = np.sum(np.abs(new_state - state))
            state = new_state
            
            if diff == 0:
                break
                
        return state, energy_history
