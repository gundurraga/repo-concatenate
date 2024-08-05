import os
import gitignore_parser

# Directory containing the repository (current directory by default)
repo_dir = '.'  # Adjust this path if needed

# Output file
output_file = 'all_files_concatenated.txt'

# Name of this script
script_name = os.path.basename(__file__)

# Function to read and parse .gitignore


def parse_gitignore(file_path):
    if os.path.exists(file_path):
        gitignore = gitignore_parser.parse_gitignore(file_path)
        return gitignore
    return None


# Parse the .gitignore file
gitignore_path = os.path.join(repo_dir, '.gitignore')
gitignore = parse_gitignore(gitignore_path)

if gitignore is None:
    print("No .gitignore file found. Proceeding without ignoring any files.")

with open(output_file, 'w', encoding='utf-8') as outfile:
    for root, dirs, files in os.walk(repo_dir):
        # Skip .git directory and its contents
        if '.git' in dirs:
            dirs.remove('.git')

        # Remove ignored directories based on .gitignore
        if gitignore:
            dirs[:] = [d for d in dirs if not gitignore(os.path.join(root, d))]

        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, repo_dir)
            if (gitignore is None or not gitignore(file_path)) and file_path != output_file and file != script_name:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                    outfile.write(f"\n########### {rel_path} ###########\n\n")
                    outfile.write(infile.read())
                    outfile.write(f"\n--- End of {rel_path} ---\n")

print(f"All files have been concatenated into {output_file}")
