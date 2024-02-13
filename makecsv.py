from Bio import Entrez, SeqIO
import os
import re
import csv
from tqdm import tqdm

# Email for searching NCBI database
Entrez.email = "example@drexel.edu"

# Create csv file for storing database results
csv_file = open('sequence_files.csv', mode='a', newline='')
writer = csv.writer(csv_file)

# Path of "sequences" folder
directory_path = r'C:\...\sequences'

# Get list of folders within "sequences"
for folder_name in tqdm(os.listdir(directory_path)):
    folder_path = os.path.join(directory_path, folder_name)
    if os.path.isdir(folder_path):
        # Get list of files in each folder
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path) and file_name.endswith('.fna'):
                with open(file_path, 'r') as file:
                    file_contents = file.read()

                # Get NCBI refrence sequence from beginning of file
                pattern = r'>\s*([^ ]+)'
                match = re.search(pattern, file_contents)
                ncbi_ref = match.group(1)

                # Search NCBI for refrence sequence
                handle = Entrez.esearch(db='nucleotide', term=ncbi_ref)
                records = Entrez.read(handle)
                handle = Entrez.efetch(
                    db='nucleotide', id=records['IdList'][0], rettype='gb', retmode='text')
                record = SeqIO.read(handle, 'genbank')

                # Get the taxonomy domains for each genome and make list
                # Order of columns:
                # Folder Name, File Name, NCBI Ref Seq, Taxonomy Levels
                new_row = [folder_name, file_name, ncbi_ref]
                new_row.extend(record.annotations['taxonomy'])

                # Write list to csv file
                writer.writerow(new_row)
