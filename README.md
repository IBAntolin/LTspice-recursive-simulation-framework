## LTspice-recursive-simulation-framework
Python based automated LTspice simulation workflow for recursive processing of .txt PWL input signals, including raw data parsing and CREMAT front-end electronics examples.

## Overview
This repository provides a Python-based workflow for automating LTspice simulations using externally generated Piecewise Linear (PWL) current input files.

The input `.txt` waveform files are generated from GARFIELD simulations of signals produced by an Fe55 X-ray source inside a spherical gaseous detector.

The workflow includes:

- Preprocessing of waveform `.txt` files
- Recursive/batch LTspice simulations
- Multi-channel signal handling
- Automatic `.raw` file generation
- Parsing of LTspice `.raw` outputs into readable `.txt` data files
- Example electronics chain using a CREMAT amplifier and shaper circuit in `.asc` format

This repository was developed for automated simulations of detector front-end electronics using CREMAT amplifier and shaping circuits.

The input signals originate from GARFIELD simulations of Fe55 X-ray interactions inside a spherical gaseous detector, producing multi-channel current waveforms that are processed and injected into LTspice for electronics response simulations.

Although originally designed for gaseous detector studies, the framework can be adapted for other applications requiring recursive or batch LTspice simulations with externally generated input signals.

## LTspice Requirements
This environment assumes that:

- `LTspice.exe`
- `cremat_eval_board.asc`
-  folder with input files

are located in the same directory as the Python scripts.

The LTspice executable path is currently hardcoded in the scripts as:

```python
exe_path = os.path.join(base_dir, "LTspice.exe")

## Step-by-Step Execution
1. Prepare Input Files

Place your raw event files in the folder:
- **`1bar_indiv_readout_fe55_pwl/`**

Files should be named `pwl_0.txt`, `pwl_1.txt`, `pwl_2.txt`, ... and contain **12 columns** (time + 11 channels), space-separated.

---

2. Run `fixing_txt_files.py`

This script processes the raw events:
- Splits each event into individual channels
- Scales current values by ×1000
- Adds a final zero-current step (required for LTspice PWL)
- Creates one processed file per channel

```bash
python fixing_txt_files.py
