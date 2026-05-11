# import os
# import subprocess
# import re

# # Directory containing the script
# base_dir = os.path.dirname(os.path.abspath(__file__))

# # Define paths
# asc_file = os.path.join(base_dir, "cremat_eval_board.asc")
# exe_path = os.path.join(base_dir, "LTspice.exe")
# pwl_folder = os.path.join(base_dir, "pwl_fe55_far")
# raw_folder = os.path.join(base_dir, "raw_files_fe55")

# # Check if required files and directories exist
# if not os.path.exists(asc_file):
    
#     print(f"Error: ASC file 'cremat_eval_board.asc' does not exist.")
#     exit(1)

# if not os.path.exists(exe_path):
#     print(f"Error: LTspice executable 'LTspice.exe' does not exist.")
#     exit(1)

# if not os.path.exists(pwl_folder):
#     print(f"Error: Input directory 'pwl_files' does not exist.")
#     exit(1)

# # Ensure raw_files folder exists
# if not os.path.exists(raw_folder):
#     os.makedirs(raw_folder)
#     print(f"Created output directory: {os.path.relpath(raw_folder, base_dir)}")

# # Check if pwl_folder is writable (needed for file renaming)
# if not os.access(pwl_folder, os.W_OK):
#     print(f"Error: No write permission for input directory 'pwl_files'. Try running as administrator or moving to a writable directory (e.g., Documents).")
#     exit(1)

# # Check if raw_folder is writable
# if not os.access(raw_folder, os.W_OK):
#     print(f"Error: No write permission for output directory 'raw_files. Try running as administrator or moving to a writable directory (e.g., Documents).")
#     exit(1)

# # Step 1: Collect input files (current.txt or pwl_*_processed.txt)
# input_files = []
# for file_name in os.listdir(pwl_folder):
#     if file_name == "current.txt" or (file_name.startswith("pwl") and file_name.endswith("_processed.txt")):
#         input_file = os.path.join(pwl_folder, file_name)
#         input_files.append(input_file)

# # Sort files numerically by extracting the number from the file name
# def get_file_number(file_path):
#     file_name = os.path.basename(file_path)
#     if file_name == "current.txt":
#         return 0  # Assign 0 to current.txt
#     match = re.search(r'pwl_(\d+)_processed\.txt', file_name)
#     return int(match.group(1)) if match else float('inf')  # Invalid files go to the end

# input_files.sort(key=get_file_number)  # Sort by numerical value
# print(f"Found {len(input_files)} input files to simulate: {[os.path.relpath(f, base_dir) for f in input_files]}")

# # Step 2: Simulation loop
# for input_file in input_files:
#     rel_input_file = os.path.relpath(input_file, base_dir)
#     temp_file = os.path.join(pwl_folder, "current.txt")
#     rel_temp_file = os.path.relpath(temp_file, base_dir)

#     # Extract number from input file name 
#     file_name = os.path.basename(input_file)
#     if file_name == "current.txt":
#         sim_number = "0"  # Default number for current.txt
#     else:
#         match = re.search(r'pwl_(\d+)_processed\.txt', file_name)
#         if match:
#             sim_number = match.group(1)  # Extract the number (e.g., '1', '2')
#         else:
#             print(f"Warning: Could not extract number from {rel_input_file}. Skipping.")
#             continue

#     # Define output .raw file name using the extracted number
#     output_raw = os.path.join(raw_folder, f"simulation{sim_number}_far.raw")
#     rel_output_raw = os.path.relpath(output_raw, base_dir)

#     print(f"Processing simulation {sim_number} with {rel_input_file}")

#     # Remove existing current.txt to avoid conflict
#     if os.path.exists(temp_file) and input_file != temp_file:
#         try:
#             os.remove(temp_file)
#             print(f"Removed existing {rel_temp_file} to avoid conflict")
#         except PermissionError as pe:
#             print(f"PermissionError: Unable to remove {rel_temp_file}. {pe}")
#             print("Try running the script as administrator or checking file permissions.")
#             continue
#         except Exception as e:
#             print(f"Error removing {rel_temp_file}: {e}")
#             continue

#     # Rename input file to current.txt (unless it's already current.txt)
#     if input_file != temp_file:
#         try:
#             os.rename(input_file, temp_file)
#             print(f"Renamed {rel_input_file} to {rel_temp_file}")
#         except PermissionError as pe:
#             print(f"PermissionError: Unable to rename {rel_input_file} to {rel_temp_file}. {pe}")
#             print("Try running the script as administrator or checking file permissions.")
#             continue
#         except Exception as e:
#             print(f"Error renaming {rel_input_file} to {rel_temp_file}: {e}")
#             continue

#     # Run simulation
#     cmd = [exe_path, "-b", asc_file]
#     print(f"Running simulation with command: {' '.join(cmd)}")
#     try:
#         result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         if result.returncode == 0:
#             # Move the generated .raw file
#             raw_default = os.path.splitext(asc_file)[0] + ".raw"
#             rel_raw_default = os.path.relpath(raw_default, base_dir)
#             if os.path.exists(raw_default):
#                 try:
#                     os.rename(raw_default, output_raw)
#                     print(f"Moved {rel_raw_default} to {rel_output_raw}")
#                 except PermissionError as pe:
#                     print(f"PermissionError: Unable to move {rel_raw_default} to {rel_output_raw}. {pe}")
#                     print("Try running the script as administrator or checking file permissions.")
#                 except Exception as e:
#                     print(f"Error moving {rel_raw_default} to {rel_output_raw}: {e}")
#             else:
#                 print(f"Warning: Simulation output {rel_raw_default} not found")
#         else:
#             print(f"Simulation failed for {rel_output_raw}: {result.stderr.decode()}")
#     except Exception as e:
#         print(f"Error running simulation for {rel_output_raw}: {e}")

#     # If input was current.txt, rename it to pwl_0_processed.txt
#     if input_file == temp_file:
#         new_file_name = os.path.join(pwl_folder, f"pwl_0_processed.txt")
#         rel_new_file_name = os.path.relpath(new_file_name, base_dir)
#         if os.path.exists(new_file_name):
#             print(f"Warning: {rel_new_file_name} already exists, skipping rename to avoid overwrite.")
#         else:
#             try:
#                 os.rename(temp_file, new_file_name)
#                 print(f"Renamed {rel_temp_file} to {rel_new_file_name}")
#             except PermissionError as pe:
#                 print(f"PermissionError: Unable to rename {rel_temp_file} to {rel_new_file_name}. {pe}")
#                 print("Try running the script as administrator or checking file permissions.")
#             except Exception as e:
#                 print(f"Error renaming {rel_temp_file} to {rel_new_file_name}: {e}")
#     # Otherwise, rename current.txt back to original name (for pwl_*_processed.txt files)
#     else:
#         try:
#             os.rename(temp_file, input_file)
#             print(f"Renamed {rel_temp_file} back to {rel_input_file}")
#         except PermissionError as pe:
#             print(f"PermissionError: Unable to rename {rel_temp_file} back to {rel_input_file}. {pe}")
#             print("Try running the script as administrator or checking file permissions.")
#         except Exception as e:
#             print(f"Error renaming {rel_temp_file} back to {rel_input_file}: {e}")

# print("Simulations completed successfully!")


#********************* 11 channels verison *********************
import os
import subprocess
import re

# Directory containing the script
base_dir = os.path.dirname(os.path.abspath(__file__))

# Define paths
asc_file = os.path.join(base_dir, "cremat_eval_board.asc")
exe_path = os.path.join(base_dir, "LTspice.exe")
pwl_folder = os.path.join(base_dir, "1bar_indiv_readout_fe55_pwl_processed")
raw_folder = os.path.join(base_dir, "1bar_indiv_readout_fe55_raw")

# ----------------------------------------------------------------------
# Checks
# ----------------------------------------------------------------------

if not os.path.exists(asc_file):
    print("Error: ASC file 'cremat_eval_board.asc' does not exist.")
    exit(1)

if not os.path.exists(exe_path):
    print("Error: LTspice executable 'LTspice.exe' does not exist.")
    exit(1)

if not os.path.exists(pwl_folder):
    print("Error: Input directory does not exist.")
    exit(1)

os.makedirs(raw_folder, exist_ok=True)

if not os.access(pwl_folder, os.W_OK):
    print("Error: No write permission for PWL directory.")
    exit(1)

if not os.access(raw_folder, os.W_OK):
    print("Error: No write permission for RAW directory.")
    exit(1)

# ----------------------------------------------------------------------
# Collect PWL files grouped by event and channel
# ----------------------------------------------------------------------

pwl_files = {}  # {event: {channel: filepath}}
pattern = re.compile(r"pwl_(\d+)_ch_(\d+)_processed\.txt")

for fname in os.listdir(pwl_folder):
    match = pattern.match(fname)
    if not match:
        continue

    event = int(match.group(1))
    channel = int(match.group(2))
    pwl_files.setdefault(event, {})[channel] = os.path.join(pwl_folder, fname)

if not pwl_files:
    print("Error: No valid pwl_<event>_ch_<channel>_processed.txt files found.")
    exit(1)

print(f"Found {len(pwl_files)} events.")

# ----------------------------------------------------------------------
# Simulation loop (event × channel)
# ----------------------------------------------------------------------

temp_file = os.path.join(pwl_folder, "current.txt")

for event in sorted(pwl_files.keys()):
    for channel in sorted(pwl_files[event].keys()):
        input_file = pwl_files[event][channel]
        rel_input = os.path.relpath(input_file, base_dir)

        output_raw = os.path.join(
            raw_folder,
            f"simulation_evt{event}_ch{channel}.raw"
        )
        rel_output = os.path.relpath(output_raw, base_dir)

        print(f"\nSimulating event {event}, channel {channel}")
        print(f"Using input: {rel_input}")

        # Remove existing current.txt if present
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception as e:
                print(f"Error removing existing current.txt: {e}")
                continue

        # Rename PWL file to current.txt
        try:
            os.rename(input_file, temp_file)
        except Exception as e:
            print(f"Error renaming {rel_input} to current.txt: {e}")
            continue

        # Run LTspice
        cmd = [exe_path, "-b", asc_file]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            print(f"Simulation failed: {result.stderr.decode().strip()}")
        else:
            raw_default = os.path.splitext(asc_file)[0] + ".raw"
            if os.path.exists(raw_default):
                try:
                    os.rename(raw_default, output_raw)
                    print(f"Saved output: {rel_output}")
                except Exception as e:
                    print(f"Error moving .raw file: {e}")
            else:
                print("Warning: Expected .raw file not found.")

        # Restore original PWL filename
        try:
            os.rename(temp_file, input_file)
        except Exception as e:
            print(f"Error restoring original PWL file: {e}")

print("\nAll simulations completed.")
