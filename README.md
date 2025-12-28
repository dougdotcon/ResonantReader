


**ROLE:**
You are an Expert Frontend Engineer and UI/UX Designer specializing in Data Visualization and "Scientific/Futuristic" interfaces (think Sci-Fi HUDs, Obsidian Graph, Minority Report).

**TASK:**
Create a **Single File Prototype (index.html)** for a Micro-SaaS called **"Resonant Reader"**.
This app allows users to upload a PDF (simulated) and visualizes the text not as pages, but as a **Dynamic Neural Network of Concepts**.

**TECHNICAL CONSTRAINTS:**
1.  **Single File:** All CSS, JS, and HTML in one file.
2.  **No External heavy deps:** Use Vanilla JS and HTML5 Canvas for the graph. You MAY use a CDN link for a lightweight physics engine like `d3.js` or write a simple custom force-directed graph loop (preferred for "wow" factor).
3.  **Aesthetic:** Dark Mode (`#0a0a0a`), Neon Accents (Cyan/Purple), Glassmorphism. Font: `Inter` or `Roboto Mono`.

**CORE FEATURES TO IMPLEMENT:**
1.  **The "Cortex" (Main Canvas):**
    *   A central interactive visualization of nodes (Concepts).
    *   Nodes should float gently (simulating oscillators).
    *   When the user hovers a node (e.g., "Entropy"), it should GLOW and light up connected nodes (e.g., "Chaos", "Time") via distinct shiny lines. This represents "Resonance".
2.  **The "Reader" (Sidebar):**
    *   A simulated text panel on the right.
    *   When a node is clicked in the graph, the text panel automatically scrolls to the relevant paragraph and highlights the keywords.
3.  **Status HUD:**
    *   Small indicators showing "System Entropy: Low", "Resonance: 98%".

**MOCK DATA (Use this in the JS):**
Create a mock dataset of a book about "Physics of Consciousness".
*   Nodes: [Entropy, Time, Consciousness, Gravity, AI, Evolution, Resonance].
*   Links: {Entropy-Time}, {Consciousness-AI}, {Resonance-Gravity}, {Evolution-Entropy}.

**VISUAL STYLE:**
*   Background: Deep void black.
*   Nodes: Glowing orbs.
*   Links: Thin, pulsing energy beams.
*   The UI should feel "Alive" and "Breathing".

**OUTPUT:**
Provide the complete, bug-free `index.html` code.
