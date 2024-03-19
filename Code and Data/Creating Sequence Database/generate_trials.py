import os
import shutil
import random
import csv


# Change to the desired location of the main directory that each trial will be in
trial_loc = r"C:\...\trials"

# Change to location of testnumberrows.csv (created by make_test_row_index.py)
testrows_dir = r"C:\...\testnumberrows.csv"

# Change to location of testing sequence main file (seq.fna)
seq_dir = r"C:\...\testing_sequence\seq.fna"

# Change to location of sequences directory containing folders with each read
sequence_dir = r"C:\...\sequences"


# Create /folder/subfolder/ directories
def create_folders(parent_folders, subfolders):
    for parent_folder in parent_folders:
        try:
            os.makedirs(parent_folder)
        except FileExistsError:
            pass
        
        for subfolder in subfolders:
            subfolder_path = os.path.join(parent_folder, subfolder)
            try:
                os.makedirs(subfolder_path)
            except FileExistsError:
                pass

# Convert txt file to list
def read_numbers_from_file(filename):
    numbers = []
    with open(filename, 'r') as file:
        for line in file:
            # Strip leading/trailing whitespace and check if line is not empty
            line = line.strip()
            if line:
                try:
                    # Try converting line to integer
                    number = int(line)
                    numbers.append(number)
                except ValueError:
                    # Ignore non-numeric lines
                    pass
    return list(set(numbers))  # Convert to set to remove duplicates, then back to list

# Read each txt file within a folder and convert each file into a list, then combine all lists into a dictionary
def read_numbers_from_folder(folder):
    all_groups = {}
    for filename in os.listdir(folder):
        if filename.endswith('.txt'):
            # Extract the word prefix and number from the filename
            file_parts = filename.split('far')[0].split('txt')[0]
            prefix = ''.join(filter(str.isalpha, file_parts))
            number = ''.join(filter(str.isdigit, file_parts))
            key = f"{prefix}"
            subgroup_key = f"{number}"
            if key not in all_groups:
                all_groups[key] = {}
            if subgroup_key not in all_groups[key]:
                all_groups[key][subgroup_key] = {}
            file_type = "far" if "far" in filename else "base"
            all_groups[key][subgroup_key][file_type] = read_numbers_from_file(os.path.join(folder, filename))
    return all_groups

# Randomly split a list in half and make the second list 10 random values from its half
def split_list(input_list):
    random.shuffle(input_list)
    half_length = len(input_list) // 2
    list_a = input_list[:half_length]
    remaining_half = input_list[half_length:]
    
    # If the number of items in the original list is odd, put the odd value into list_a
    if len(input_list) % 2 != 0:
        if len(list_a) % 2 == 0:
            list_a.append(remaining_half.pop())

    # Take the remaining half (not in list_a) and randomly pick 10 values to be in list_b
    random.shuffle(remaining_half)
    list_b = remaining_half[:10]
    
    return list_a, list_b

# Randomly pick 10 values from a list
def random_pick(input_list):
    if len(input_list) <= 10:
        return input_list
    else:
        return random.sample(input_list, 10)

# Randomly picks X% (as a decimal) of items in a list for a new list
def select_percentage_of_list(input_list, percentage):
    if not (0 <= percentage <= 1):
        raise ValueError("Percentage should be between 0 and 1")

    num_items_to_select = int(len(input_list) * percentage)
    selected_items = random.sample(input_list, num_items_to_select)
    return selected_items

# Take a list of folders and copy their contents to a new folder
def copy_files_to_new_folder(folder_list, source_directory, destination_folder):
    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    # Iterate through each folder in the list
    for folder_name in folder_list:
        # Convert folder_name to a string if it's not already
        folder_name = str(folder_name)
        
        # Get the full path of the folder
        full_folder_path = os.path.join(source_directory, folder_name)
        
        # Check if the folder exists
        if not os.path.exists(full_folder_path):
            print(f"Error: Folder '{full_folder_path}' does not exist.")
            continue
        
        # Get the files inside the folder
        files = os.listdir(full_folder_path)
        
        # Check if the folder contains exactly one file
        if len(files) != 1:
            print(f"Error: Folder '{full_folder_path}' does not contain exactly one file.")
            continue
        
        # Get the full path of the file to copy
        file_to_copy = os.path.join(full_folder_path, files[0])
        
        # Create a new folder with the same name as the file
        new_folder_path = os.path.join(destination_folder, folder_name)
        os.makedirs(new_folder_path, exist_ok=True)
        
        # Copy the file into the new folder
        shutil.copy(file_to_copy, new_folder_path)

# Copy specified testing sequences from the main seq.fna file, given their starting row
def copy_data_blocks(start_row, file_path):
    data_blocks = []
    block = []
    block_count = 0
    block_started = False
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            if line_number < start_row:
                continue  # Skip lines until reaching the start_row
            if not block_started and line.startswith('>') and line[1:].strip().isdigit():
                # Start of a new block
                block_started = True
            elif block_started and line.startswith('>') and line[1:].strip().isdigit():
                # Start of the next block, append the current block to data_blocks and reset for the new block
                data_blocks.extend(block)  # Extend instead of append
                block = []
                block_count += 1
                if block_count == 2:  # Stop after saving two data blocks
                    break
            if block_started:
                block.append(line.strip())
    return data_blocks

# Create dictionary of the sequences and their respective row number in the seq.fna file
# This uses the testnumberrows.csv file made by make_test_row_index.py
def create_dictionary_from_csv(csv_file):
    # Initialize an empty dictionary to store the data
    data_dict = {}

    # Open the CSV file and read its contents
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')  # Assuming comma-delimited
        for row in reader:
            # Assuming the column names are combined as 'Number,Row'
            number = int(row['Number'])
            row_value = int(row['Row'])
            data_dict[number] = row_value

    return data_dict

# Creates a testing data file as a .fna from a list, where each item is a row
def write_fna_file(rows, filename):
    with open(filename, 'w') as f:
        for row in rows:
            f.write(row + '\n')

# Change to the location of the txt files with the desired training sequences for each trial
folder_path = r"C:\...\datatxt"

# Create dictionary of all txt file values
groups_of_numbers = read_numbers_from_folder(folder_path)

# Create dataset folders with files inside them, each parent folder is a unique dataset for a single trial
for level in groups_of_numbers:
    for trial in groups_of_numbers[level]:
        
        # Creates directories of the parent and sub folders for each trial
        parent_folders = [
            os.path.join(trial_loc, "{}{}_50".format(level,trial)),
            os.path.join(trial_loc, "{}{}_40".format(level,trial)),
            os.path.join(trial_loc, "{}{}_20".format(level,trial))]
        subfolders = ["train", "test_near", "test_far"]
        create_folders(parent_folders, subfolders)

        # Creates lists (of sequence folder names) for each training and testing case
        txtfiles = groups_of_numbers[level][trial]
        train50, test_near = split_list(txtfiles['base'])
        train40 = select_percentage_of_list(train50, 0.8)
        train20 = select_percentage_of_list(train50, 0.4)
        test_far = random_pick(txtfiles['far'])

        # Using testnumberrows.csv, create new testing seq.fna files based of list of testing sequences for each trial
        testrows = create_dictionary_from_csv(testrows_dir)
        test_near_seqs = []
        for x in test_near:
            test_near_seqs.extend(copy_data_blocks(testrows[x], seq_dir))
        test_far_seqs = []
        for x in test_far:
            test_far_seqs.extend(copy_data_blocks(testrows[x], seq_dir))

        # Create dataset 50
        copy_files_to_new_folder(train50, sequence_dir, os.path.join(parent_folders[0], subfolders[0]))
        write_fna_file(test_near_seqs, os.path.join(parent_folders[0], subfolders[1], "seq.fna"))
        write_fna_file(test_far_seqs, os.path.join(parent_folders[0], subfolders[2], "seq.fna"))

        # Create dataset 40
        copy_files_to_new_folder(train40, sequence_dir, os.path.join(parent_folders[1], subfolders[0]))
        write_fna_file(test_near_seqs, os.path.join(parent_folders[1], subfolders[1], "seq.fna"))
        write_fna_file(test_far_seqs, os.path.join(parent_folders[1], subfolders[2], "seq.fna"))

        # Create dataset 20
        copy_files_to_new_folder(train20, sequence_dir, os.path.join(parent_folders[2], subfolders[0]))
        write_fna_file(test_near_seqs, os.path.join(parent_folders[2], subfolders[1], "seq.fna"))
        write_fna_file(test_far_seqs, os.path.join(parent_folders[2], subfolders[2], "seq.fna"))