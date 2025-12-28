"""
Integration Script: Connects Python Backend to React Frontend (Port 3000 -> UI)
-------------------------------------------------------------------------------
This script:
1. Runs the Linguistic Resonator (prototype_text_resonator.py).
2. Extracts the Semantic Network (Words + Resonance Strength).
3. Generates the 'constants.ts' file for the React UI.
"""

import sys
import os
import json
import numpy as np

# Add current dir to path to import prototype
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engine import run_linguistic_resonance, words, associations

# Use relative path to UI constants for portability
CONSTANTS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ui", "constants.ts"))

def generate_typescript_file():
    print("[INTEGRATION] Running Resonance Simulation...")
    # Run simulation for 'King' to get dynamic resonance scores
    _, resonances = run_linguistic_resonance("King")
    
    # 1. Build Nodes
    nodes = []
    for i, word in enumerate(words):
        # Calculate 'Value' based on resonance (if it resonates, it's bigger)
        score = resonances.get(word, 0)
        size = 15 + (score * 20) # Base 15, max +20
        
        # Fake groups for demo
        group = 1
        if word in ["King", "Queen", "Man", "Woman"]: group = 1
        elif word in ["Apple", "Fruit"]: group = 2
        elif word in ["Car", "Engine"]: group = 3
        
        node = {
            "id": word,
            "group": group,
            "description": f"Resonance Score: {score:.2f}",
            "val": size
        }
        nodes.append(node)
        
    # 2. Build Links
    links = []
    for w1, w2, strength in associations:
        if strength > 0:
            link = {
                "source": w1,
                "target": w2,
                "value": strength
            }
            links.append(link)
            
    # 3. Create TS Content
    ts_content = f"""import {{ GraphData, BookSection }} from './types';

export const INITIAL_GRAPH_DATA: GraphData = {{
  nodes: {json.dumps(nodes, indent=4)},
  links: {json.dumps(links, indent=4)}
}};

export const BOOK_CONTENT: BookSection[] = [
  {{
    id: "King",
    title: "The Concept of Monarchy",
    content: "The King acts as a primary oscillator in the social hierarchy. Through history, the King node has strongly coupled with the Queen node, creating a stable frequency of governance.",
    relatedConcepts: ["King", "Queen", "Man"]
  }},
  {{
    id: "Queen",
    title: "The Consort Resonance",
    content: "Queens exhibit strong phase synchronization with Kings. This demonstrates the pairing principle in semantic linguistics, where gendered counterparts resonate at harmonic frequencies.",
    relatedConcepts: ["Queen", "Woman", "King"]
  }},
  {{
    id: "Apple",
    title: "Fruit Dynamics",
    content: "An Apple falls. Gravity pulls it. But in semantic space, Apple pulls 'Fruit' towards it. It is a high-gravity concept in the domain of nutrition.",
    relatedConcepts: ["Apple", "Fruit", "Gravity"]
  }}
];
"""
    # Fix JSON keys to be valid JS object keys (optional, but JSON strings are fine in TS usually if type matches)
    # Actually, JSON.dumps produces "key": "value". TS objects are key: "value". 
    # But valid JSON is valid JS/TS object literal.
    
    print(f"[INTEGRATION] Writing to {CONSTANTS_PATH}...")
    with open(CONSTANTS_PATH, "w", encoding="utf-8") as f:
        f.write(ts_content)
        
    print("[SUCCESS] Backend connected to Frontend.")

if __name__ == "__main__":
    generate_typescript_file()
