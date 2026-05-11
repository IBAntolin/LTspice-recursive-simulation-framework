# import os

# # Directory containing the script
# script_directory = os.path.dirname(os.path.abspath(__file__))

# # Input and output directories
# input_directory = os.path.join(script_directory, "pwl_single_elec")
# output_directory_far = os.path.join(script_directory, "pwl_single_elec_far")
# output_directory_near = os.path.join(script_directory, "pwl_single_elec_near")

# # Check directories
# for d in [input_directory, output_directory_far, output_directory_near]:
#     if not os.path.exists(d):
#         print(f"Error: Directory '{os.path.basename(d)}' does not exist.")
#         exit(1)
#     if not os.access(d, os.W_OK):
#         print(f"Error: No write permission for directory '{os.path.basename(d)}'.")
#         exit(1)

# # Clear previous processed files
# for out_dir in [output_directory_far, output_directory_near]:
#     try:
#         for file_name in os.listdir(out_dir):
#             if file_name.startswith("pwl") and file_name.endswith("_processed.txt"):
#                 os.remove(os.path.join(out_dir, file_name))
#                 print(f"Cleared {file_name} in {os.path.basename(out_dir)}")
#     except Exception as e:
#         print(f"Warning: Could not clear {os.path.basename(out_dir)}: {e}")

# # Collect valid files
# valid_files = [f for f in os.listdir(input_directory) if f.startswith("pwl") and f.endswith(".txt")]
# print(f"Found {len(valid_files)} valid files to process.")

# # Counter for processed files (ensures continuous numbering)
# processed_index = 0
# skipped_files = []

# # Process files
# for file_name in valid_files:
#     input_file = os.path.join(input_directory, file_name)

#     try:
#         with open(input_file, "r", encoding="utf-8") as f:
#             lines = f.readlines()
#     except Exception as e:
#         print(f"Error reading {file_name}: {e}")
#         skipped_files.append(file_name)
#         continue

#     if not lines or len(lines) < 2:
#         print(f"Warning: {file_name} has insufficient data, skipping.")
#         skipped_files.append(file_name)
#         continue

#     # Output file paths using continuous processed_index
#     output_file_far = os.path.join(output_directory_far, f"pwl_{processed_index}_processed.txt")
#     output_file_near = os.path.join(output_directory_near, f"pwl_{processed_index}_processed.txt")

#     # Skip header
#     data_lines = lines[1:]

#     far_lines = []
#     near_lines = []
#     seen_times = set()

#     for line in data_lines:
#         parts = line.strip().split(",")
#         if len(parts) < 4:
#             continue

#         time_val = parts[1].strip()

#         # Skip duplicate times
#         if time_val in seen_times:
#             continue
#         seen_times.add(time_val)

#         try:
#             far_val = float(parts[2])
#             near_val = parts[3]
#         except ValueError:
#             continue

#         far_lines.append(f"{time_val} {far_val}\n")
#         near_lines.append(f"{time_val} {near_val}\n")

#     # Append last step with zero
#     try:
#         last_time = float(data_lines[-1].split(",")[1].rstrip("n"))
#         second_last_time = float(data_lines[-2].split(",")[1].rstrip("n")) if len(data_lines) > 2 else last_time - 1.0
#         time_step = last_time - second_last_time if second_last_time is not None else 1.0
#         next_time = last_time + time_step
#         far_lines.append(f"{int(next_time)}n 0.0\n")
#         near_lines.append(f"{int(next_time)}n 0.0\n")
#     except Exception as e:
#         print(f"Error computing extra time step in {file_name}: {e}")
#         skipped_files.append(file_name)
#         continue

#     # Write far output
#     try:
#         with open(output_file_far, "w", encoding="utf-8") as f:
#             f.writelines(far_lines)
#         print(f"Processed FAR: {file_name} -> {os.path.basename(output_file_far)}")
#     except Exception as e:
#         print(f"Error writing FAR file for {file_name}: {e}")
#         skipped_files.append(file_name)
#         continue

#     # Write near output
#     try:
#         with open(output_file_near, "w", encoding="utf-8") as f:
#             f.writelines(near_lines)
#         print(f"Processed NEAR: {file_name} -> {os.path.basename(output_file_near)}")
#     except Exception as e:
#         print(f"Error writing NEAR file for {file_name}: {e}")
#         skipped_files.append(file_name)
#         continue

#     processed_index += 1  # increment only after successful processing

# # Rename first processed file in FAR and NEAR to current.txt
# for out_dir in [output_directory_far, output_directory_near]:
#     first_output_file = os.path.join(out_dir, "pwl_0_processed.txt")
#     current_file = os.path.join(out_dir, "current.txt")
#     if os.path.exists(first_output_file):
#         try:
#             os.rename(first_output_file, current_file)
#             print(f"Renamed {os.path.basename(first_output_file)} -> current.txt in {os.path.basename(out_dir)}")
#         except Exception as e:
#             print(f"Error renaming {first_output_file} to current.txt: {e}")
#     elif processed_index > 0:
#         print(f"Warning: {first_output_file} not found, no file renamed.")

# print(f"\nProcessing complete. Successfully processed {processed_index}/{len(valid_files)} files.")
# if skipped_files:
#     print(f"Skipped files: {', '.join(skipped_files)}")


#********************* 11 channels verison *********************
import os

# Directory containing the script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Input and output directories
input_directory = os.path.join(script_directory, "1bar_indiv_readout_fe55_pwl")
output_directory = os.path.join(script_directory, "1bar_indiv_readout_fe55_pwl_processed")

os.makedirs(output_directory, exist_ok=True)

if not os.path.exists(input_directory):
    print(f"Error: Directory '{os.path.basename(input_directory)}' does not exist.")
    exit(1)

# Clear previous processed files
for file_name in os.listdir(output_directory):
    if file_name.endswith("_processed.txt") or file_name == "current.txt":
        os.remove(os.path.join(output_directory, file_name))

# Collect valid input files
valid_files = sorted(
    f for f in os.listdir(input_directory)
    if f.startswith("pwl") and f.endswith(".txt")
)

print(f"Found {len(valid_files)} valid files.")

# Number of channels (columns 1–11)
NUM_CHANNELS = 11

# Process each event file independently
for file_name in valid_files:
    input_file = os.path.join(input_directory, file_name)
    event_name = os.path.splitext(file_name)[0]  # e.g. pwl_0

    # One list per channel for this event
    channel_data = {ch: [] for ch in range(NUM_CHANNELS)}
    seen_times = set()

    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if len(lines) < 2:
        print(f"Skipping {file_name}: insufficient data")
        continue

    # Parse data lines
    for line in lines[1:]:
        parts = line.strip().split()
        if len(parts) != 12:
            continue

        time_val = parts[0]

        # Skip duplicate times within this event
        if time_val in seen_times:
            continue
        seen_times.add(time_val)

        currents = parts[1:]

        for ch in range(NUM_CHANNELS):
            try:
                scaled_current = float(currents[ch]) * 1000.0 #remove this: test
            except ValueError:
                continue

            channel_data[ch].append(f"{time_val} {scaled_current}\n")

    # Append final zero step per channel
    for ch, data in channel_data.items():
        if len(data) < 2:
            continue

        last_time = float(data[-1].split()[0].rstrip("n"))
        prev_time = float(data[-2].split()[0].rstrip("n"))
        dt = last_time - prev_time

        next_time = int(last_time + dt)
        data.append(f"{next_time}n 0.0\n")

    # Write output files
    for ch, data in channel_data.items():
        if not data:
            continue

        output_file = os.path.join(
            output_directory,
            f"{event_name}_ch_{ch}_processed.txt"
        )

        with open(output_file, "w", encoding="utf-8") as f:
            f.writelines(data)

        print(f"Written {event_name}_ch_{ch}_processed.txt")

# Rename pwl_0_ch_0_processed.txt -> current.txt
src = os.path.join(output_directory, "pwl_0_ch_0_processed.txt")
dst = os.path.join(output_directory, "current.txt")

if os.path.exists(src):
    if os.path.exists(dst):
        os.remove(dst)
    os.rename(src, dst)
    print("Renamed pwl_0_ch_0_processed.txt -> current.txt")
else:
    print("Warning: pwl_0_ch_0_processed.txt not found, cannot rename.")

print("\nProcessing complete.")
