# ☂️ Umbrella Corporation OS (Red Queen Mainframe)

> *"Our business is life itself."*

Welcome to the **Umbrella OS**, a highly immersive, interactive desktop environment and security mainframe built in Python using PyQt6. Designed as a simulation of the Red Queen's operating system from the *Resident Evil* universe, this project features biometric facial recognition, a procedural mechanical puzzle engine, a simulated DOS terminal, and a fully functional MDI (Multiple Document Interface) desktop.

---

## 🧬 Features

### 🔒 Security & Authentication
*   **Biometric Login:** Integrates `OpenCV` and `DeepFace` neural networks for real-time facial recognition and user authentication.
*   **Admin Override:** A fallback security protocol requiring a 3-tier authentication (User, Password, and Security Key) paired with mechanical decryption puzzles.
*   **Lethal Lockdown Sequence:** Failing authentication triggers a neuro-toxin lockdown sequence, forcing the user to solve procedural puzzles to survive.

### 🧩 Procedural Puzzle Engine
A dedicated, modular engine (`RedQueenPuzzles.py`) that dynamically generates mechanical and cryptographic challenges. Includes 10 distinct interactive puzzles:
1.  **The Mastermind:** 4-digit brute-force PIN cracker with positional telemetry.
2.  **Lights Out:** Spatial 3x3 grid balancing.
3.  **Water Jug:** Bio-chem antiserum synthesis (mathematical volume isolation).
4.  **Binary Decoder:** 8-bit to decimal translation.
5.  **Orbital Burn:** Physics/reflex timing telemetry.
6.  **Wordle (Terminal Edition):** 5-letter cryptographic key guessing.
7.  **Hash Collision:** High-speed progress bar reflex lock.
8.  **Doppler Calibrator:** Astrophysical relative velocity matching.
9.  **Logic Gate Weaver:** Boolean logic circuit completion (AND, OR, XOR).
10. **Typing Stress Test:** High-speed syntax entry under pressure.

### 🖥️ Desktop Environment
*   **MDI Workspace:** Draggable, resizable internal sub-routines simulating a classic Windows 95/XP style window manager.
*   **Dynamic Taskbar:** Tracks open processes, allowing for smooth minimizing/maximizing of internal apps.
*   **Red Queen DOS:** A fully functional, simulated command-line interface with **100+ personalized hardcoded commands**, including live animations (Matrix rain, HDD defrag simulation, Antivirus synthesis).
*   **Sub-Routines:**
    *   **File Explorer:** Browse local files with a built-in "Quarantine" system to move detected anomalies.
    *   **Virus Database:** Interactive lore databank with visual representations of bio-weapons.
    *   **Diagnostics:** Real-time CPU and RAM telemetry using `psutil`.
    *   **Surveillance:** Simulated multi-camera security feeds.
    *   **Incinerator:** A thermal deletion tool to permanently wipe selected files with a burning progress animation.
    *   **Spatial Audio / Media:** Visualizers and sliders for simulated hardware control.

---

## 🛠️ Prerequisites

To run the Umbrella OS locally, you will need **Python 3.10+** and the following dependencies:

```bash
pip install PyQt6 opencv-python deepface psutil
