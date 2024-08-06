import os
import gitignore_parser

# Directory containing the repository (current directory by default)
repo_dir = '.'  # Adjust this path if needed

# Get the name of the containing folder or repo
repo_name = os.path.basename(os.path.abspath(repo_dir))

# Output file
output_file = f'{repo_name}.txt'

# Name of this script
script_name = os.path.basename(__file__)

# Function to read and parse .gitignore


def parse_gitignore(file_path):
    if os.path.exists(file_path):
        gitignore = gitignore_parser.parse_gitignore(file_path)
        return gitignore
    return None

# Function to get folder structure, respecting .gitignore


def get_folder_structure(start_path, gitignore, output_file):
    def add_to_structure(path, prefix=''):
        entries = sorted(os.scandir(path), key=lambda e: e.name)
        entries = [e for e in entries if e.name !=
                   '.git' and e.name != output_file and e.name != script_name]
        if gitignore:
            entries = [e for e in entries if not gitignore(e.path)]

        for i, entry in enumerate(entries):
            is_last = (i == len(entries) - 1)
            if entry.is_dir():
                yield f"{prefix}{'└── ' if is_last else '├── '}{entry.name}/"
                extension = '    ' if is_last else '│   '
                yield from add_to_structure(entry.path, prefix + extension)
            else:
                yield f"{prefix}{'└── ' if is_last else '├── '}{entry.name}"

    yield f"{repo_name}/"
    yield from add_to_structure(start_path)

# Function to check if a file should be included


def should_include_file(file_path, gitignore):
    return (gitignore is None or not gitignore(file_path)) and \
        os.path.basename(file_path) != output_file and \
        os.path.basename(file_path) != script_name


# Parse the .gitignore file
gitignore_path = os.path.join(repo_dir, '.gitignore')
gitignore = parse_gitignore(gitignore_path)

if gitignore is None:
    print("No .gitignore file found. Proceeding without ignoring any files.")

# Get folder structure
folder_structure = list(get_folder_structure(repo_dir, gitignore, output_file))

with open(output_file, 'w', encoding='utf-8') as outfile:
    # Write folder structure
    outfile.write("Folder Structure:\n")
    outfile.write("\n".join(folder_structure))
    outfile.write("\n\nFile Index:\n")

    # Prepare file index
    file_index = []
    file_number = 1

    for root, dirs, files in os.walk(repo_dir):
        # Skip .git directory and its contents
        if '.git' in dirs:
            dirs.remove('.git')

        # Remove ignored directories based on .gitignore
        if gitignore:
            dirs[:] = [d for d in dirs if not gitignore(os.path.join(root, d))]

        for file in files:
            file_path = os.path.join(root, file)
            if should_include_file(file_path, gitignore):
                rel_path = os.path.relpath(file_path, repo_dir)
                file_index.append(f"{file_number}. {rel_path}")
                file_number += 1

    # Write file index
    outfile.write("\n".join(file_index))
    outfile.write("\n\n")

    # Reset file number for content
    file_number = 1

    # Write file contents
    for root, dirs, files in os.walk(repo_dir):
        if '.git' in dirs:
            dirs.remove('.git')

        if gitignore:
            dirs[:] = [d for d in dirs if not gitignore(os.path.join(root, d))]

        for file in files:
            file_path = os.path.join(root, file)
            if should_include_file(file_path, gitignore):
                rel_path = os.path.relpath(file_path, repo_dir)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                    outfile.write(
                        f"\n########### {file_number}. {rel_path} ###########\n\n")
                    outfile.write(infile.read())
                    outfile.write(
                        f"\n--- End of {file_number}. {rel_path} ---\n")
                    file_number += 1

print(f"All files have been concatenated into {output_file}")
