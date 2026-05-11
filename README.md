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

The project is intended for detector readout and front-end electronics studies, but it can be adapted for other purposes that also require recursive LTspice simulations.
