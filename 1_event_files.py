import os
import shutil

# List to store destination file paths
destination_file_paths = []

# Function to find the largest .bz2 file in a directory
def find_largest_bz2_file(directory):
    largest_file = None
    largest_size = 0

    # Iterate over all files in the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".bz2"):
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                if file_size > largest_size:
                    largest_size = file_size
                    largest_file = file_path

    return largest_file, largest_size

# Function to copy the largest .bz2 file to the appropriate directory
def copy_largest_bz2_file(source_file, destination_dir, big_files_dir, file_size):
    if source_file:
        folder_name = os.path.basename(os.path.dirname(source_file))
        filename = folder_name + ".bz2"
        if file_size > 5 * 1024 * 1024:
            destination_file = os.path.join(big_files_dir, filename)
        else:
            destination_file = os.path.join(destination_dir, filename)

        shutil.copy2(source_file, destination_file)
        destination_file_paths.append(destination_file)  # Store destination file path
        return 1
    return 0

# Recursively find the largest .bz2 file in each child folder and copy it to the appropriate directory
def find_and_copy_largest_bz2_files(directory, destination_dir, big_files_dir):
    total_files_copied = 0
    for root, dirs, files in os.walk(directory):
        if not dirs:  # If the current directory has no subdirectories, it's a leaf node
            largest_bz2_file, largest_size = find_largest_bz2_file(root)
            total_files_copied += copy_largest_bz2_file(largest_bz2_file, destination_dir, big_files_dir, largest_size)
    return total_files_copied

# Main function to start the process
def main():
    source_dir = "/Users/noahroni/Documents/ADVANCED/2020/Jul/"
    destination_dir = "/Users/noahroni/Documents/Market_Folders"
    big_files_dir = "/Users/noahroni/Documents/event_files_big"

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    if not os.path.exists(big_files_dir):
        os.makedirs(big_files_dir)

    total_files_copied = find_and_copy_largest_bz2_files(source_dir, destination_dir, big_files_dir)
    print(f"Total files copied: {total_files_copied}")

    # Print destination file paths
    #print("Destination file paths:")
    #for file_path in destination_file_paths:
    #    print(file_path)

# Run the main function
if __name__ == "__main__":
    main()
#print(destination_file_paths[0])
