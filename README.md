# Umbrella Corporation OS (Red Queen Mainframe)

> *"Our business is life itself."*

Welcome to the **Umbrella OS**, a highly immersive, interactive desktop environment and security mainframe built in Python using PyQt6. Designed as a simulation of the Red Queen's operating system from the *Resident Evil* universe, this project features biometric facial recognition, a procedural mechanical puzzle engine, a simulated DOS terminal, and a fully functional MDI (Multiple Document Interface) desktop.

---

## Features

### Security & Authentication
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

###  Desktop Environment
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

##  Prerequisites

To run the Umbrella OS locally, you will need **Python 3.10+** and the following dependencies:

```bash
pip install PyQt6 opencv-python deepface psutil
```
Installation & Setup
Clone the repository:

```Bash
git clone [https://github.com/yourusername/umbrella-os.git](https://github.com/yourusername/umbrella-os.git)
cd umbrella-os
```

2. **Asset Configuration (Important):**
   This OS relies on several specific media assets (images, gifs, and audio files) to function seamlessly. By default, the code references paths on a `D:\` drive. 
   
   *You must update the file paths in `Umbrella.py` to match your local machine, or place the appropriate assets in the designated directories.*
   
   **Required Assets:**
   *   `Umbrella_Corporation_logo.svg.png` (Primary Logo)
   *   `you_are_dead.jpg` & `blood_splash.png` (Lockdown Screens)
   *   `cam1.gif` to `cam4.gif` (Surveillance Sub-routine)
   *   `.wav` audio files (`hdd_boot.wav`, `clunk.wav`, `neuro_toxin.wav`, etc.)

3. **Initialize the Database:**
   The OS will automatically generate a blank `UMBRELLA_DB.json` file in your system's `Documents` folder upon first boot.

4. **Run the OS:**
   ```bash
   python Umbrella.py
   ```
###Usage Guidelines

      First Boot & Registration
      Upon launching, the system will enter the BIOS and Splash Screen. Navigate to the Registration Screen (bypassing the lockdown if necessary) to create your employee profile. You will input your data, receive a 4-         digit Security Key, and the system will capture your biometric face signature via webcam.
      
      Default Admin Credentials
      If you are locked out, you can access the Override protocol using the hardcoded administrator credentials:
      
      User ID: UMB-ADMIN
      
      Access Code: REDQUEEN
      
      Security Key: 7680
      
      Accessing the system via Admin Override will require you to beat 5 randomly generated mechanical puzzles.

###⚠️ Disclaimer
This is a fan-made project created for educational and entertainment purposes. "Resident Evil", "Umbrella Corporation", and "Red Queen" are trademarks of Capcom Co., Ltd.

Security Notice: The "Incinerator" sub-routine utilizes os.remove(). Files deleted using this tool are permanently removed from your system and do not go to the Recycle Bin. Use with caution.
