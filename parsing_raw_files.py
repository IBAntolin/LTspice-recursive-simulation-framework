import os
import re
from PyLTSpice import RawRead

# Directory containing the script
base_dir = os.path.dirname(os.path.abspath(__file__))

# Define paths
raw_folder = os.path.join(base_dir, "raw_files_fe55")
output_folder = os.path.join(base_dir, "1bar_long_fe55_output_files")

# Check if raw folder exists
if not os.path.exists(raw_folder):
    print(f"Error: Input directory does not exist.")
    exit(1)

# Ensure output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Created output directory: {os.path.relpath(output_folder, base_dir)}")

# Check if output folder is writable
if not os.access(output_folder, os.W_OK):
    print(f"Error: No write permission for output directory '{os.path.relpath(output_folder, base_dir)}'. Try running as administrator or moving to a writable directory (e.g., Documents).")
    exit(1)

# Step 1: Collect all .raw files starting with "simulation" and ending with _near or _far
raw_files = []
for file_name in os.listdir(raw_folder):
    match = re.match(r'simulation(\d+)_(near|far)\.raw', file_name)
    if match:
        raw_files.append(os.path.join(raw_folder, file_name))

# Sort files by simulation number, then near/far
def get_file_sort_key(file_path):
    file_name = os.path.basename(file_path)
    match = re.match(r'simulation(\d+)_(near|far)\.raw', file_name)
    if match:
        number = int(match.group(1))
        suffix = match.group(2)
        return (number, 0 if suffix == "near" else 1)  # near first, far second
    return (float('inf'), 0)

raw_files.sort(key=get_file_sort_key)
print(f"Found {len(raw_files)} .raw files to process: {[os.path.relpath(f, base_dir) for f in raw_files]}")

# Step 2: Process each .raw file
for raw_path in raw_files:
    rel_raw_path = os.path.relpath(raw_path, base_dir)

    # Extract simulation number and suffix
    file_name = os.path.basename(raw_path)
    match = re.match(r'simulation(\d+)_(near|far)\.raw', file_name)
    if match:
        sim_number = match.group(1)
        suffix = match.group(2)
    else:
        print(f"Warning: Could not extract number and suffix from {rel_raw_path}. Skipping.")
        continue

    # Define output .txt file name
    output_file = f"simulation{sim_number}_{suffix}.txt"
    output_path = os.path.join(output_folder, output_file)
    rel_output_path = os.path.relpath(output_path, base_dir)

    if os.path.exists(raw_path):
        # Read the .raw file
        try:
            ltr = RawRead(raw_path)
        except Exception as e:
            print(f"Error reading {rel_raw_path}: {e}")
            continue

        # Get the traces
        time = ltr.get_axis()
        v_out1 = ltr.get_trace("V(output1)")
        v_out2 = ltr.get_trace("V(output2)")

        if len(time) > 0:  # Check if traces are valid
            data = [(t, v1, v2) for t, v1, v2 in zip(time, v_out1, v_out2)]

            # Write data to text file with header and tab-separated columns
            try:
                with open(output_path, "w", encoding='utf-8') as f:
                    f.write("time\tV(output1)\tV(output2)\n")  # Header
                    for t, v1, v2 in data:
                        f.write(f"{t:.15e}\t{v1:.15e}\t{v2:.15e}\n")  # High precision
                print(f"Saved {rel_output_path} with time, V(output1), and V(output2)")
            except PermissionError as e:
                print(f"PermissionError: Unable to write to {rel_output_path}. {e}")
                print("Try running the script as administrator or checking file permissions.")
            except Exception as e:
                print(f"Error writing to {rel_output_path}: {e}")
        else:
            print(f"Could not find all traces (time, V(output1), V(output2)) in {rel_raw_path}. Please check the .raw file in LTspice GUI for correct trace names.")
    else:
        print(f"File not found: {rel_raw_path}")

print("Parsing completed successfully!")
