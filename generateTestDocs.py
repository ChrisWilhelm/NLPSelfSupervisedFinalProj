import os
import pandas as pd
import random

def extract_id_from_filename(filename):
    # Extract ID number from the filename
    return filename.split("_")[1]

def categorize_ids(folder_path):
    d1_ids = []
    d2_ids = []
    d1_file_names = []
    
    # Check if the provided path is a directory
    if not os.path.isdir(folder_path):
        print(f"{folder_path} is not a valid directory.")
        return d1_ids, d2_ids
    
    # Get a list of all files in the directory
    files = os.listdir(folder_path)
    
    # Categorize IDs based on file names
    for file_name in files:
        if file_name.endswith("_d1.txt"):
            d1_file_names.append(file_name)
            d1_ids.append(extract_id_from_filename(file_name))
        elif file_name.endswith("_d2.txt"):
            d2_ids.append(extract_id_from_filename(file_name))
    print(d1_file_names)
    
    return d1_ids, d2_ids

# Example usage
folder_path = "./TrainDocs_1"
d1_ids, d2_ids = categorize_ids(folder_path)

print("IDs in d1 files:", d1_ids)
print("IDs in d2 files:", d2_ids)


# Load the CSV file into a DataFrame
df = pd.read_csv("Resume.csv")


# Create a folder named TrainDocs_1 if it doesn't exist
folder_name = "TestDocs"
os.makedirs(folder_name, exist_ok=True)

# Iterate over the selected rows and save each 'Resume_txt' to a unique text file
for index, row in df.iterrows():
    if str(index) not in d1_ids:
        resume_text = row['Resume_str']
        filename = os.path.join(folder_name, f"resume_{index}_d1.txt")
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(resume_text)
        if (index % 100 == 0):
            print("Printed: " + str(index))

df2 = pd.read_csv("final_merged_dataset2.csv")

# Create a folder named TrainDocs_1 if it doesn't exist
folder_name = "TestDocs"
os.makedirs(folder_name, exist_ok=True)

# Iterate over the selected rows and save each 'Resume_txt' to a unique text file
for index, row in df2.iterrows():
    if str(index) not in d2_ids:
        resume_text = row['Resume']
        filename = os.path.join(folder_name, f"resume_{index}_d2.txt")
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(resume_text)
        if (index % 100 == 0):
            print("Printed: " + str(index))