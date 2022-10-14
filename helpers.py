import csv
import os

# Get name of repository from full url
def get_repo_name(repo_url):
    if repo_url:
        return repo_url.split("/")[-1].replace(".git", "")
    else:
        return None

# Get extension of file from filename
def get_file_ext(filename):
    if filename:
        return filename.split(".")[-1]
    else:
        return None

# Get complete filepath(includes extension .csv) for csv file given directory and file basename
def get_csv_filepath(dir, file_basename):
    if dir and file_basename:
        filepath = dir + "/" + file_basename + ".csv"
        return filepath
    else:
        return None

def check_dir_exists(dir):
    # Check whether dir exists or not
    fileExists = os.path.exists(dir)

    if not fileExists:
        # Create a new directory
        os.makedirs(dir)
        print("Directory is created!")
        
# Export data as csv file in the target directory
def export_to_csv(
    headers,
    data,
    filename,
    dir,
):
    filepath = get_csv_filepath(dir, filename)
    check_dir_exists(dir)

    # csv file gets created in the directory
    with open(filepath, "w", newline="") as csv_file:
        my_writer = csv.writer(csv_file, delimiter=",")

        # Write header
        my_writer.writerow(headers)

        # Write rows
        my_writer.writerows(data)
