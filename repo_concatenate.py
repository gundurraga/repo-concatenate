import os
import gitignore_parser
import collections

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

# Function to check if a file should be included


def should_include_file(file_path, gitignore):
    return (file_path != output_file and
            os.path.basename(file_path) != script_name and
            (gitignore is None or not gitignore(file_path)))

# Function to get all relevant files


def get_relevant_files(repo_dir, gitignore):
    relevant_files = []
    for root, dirs, files in os.walk(repo_dir):
        # Remove .git directory
        if '.git' in dirs:
            dirs.remove('.git')

        # Remove ignored directories
        if gitignore:
            dirs[:] = [d for d in dirs if not gitignore(os.path.join(root, d))]

        for file in files:
            file_path = os.path.join(root, file)
            if should_include_file(file_path, gitignore):
                relevant_files.append(file_path)
    return relevant_files

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

# Statistics functions


def count_total_lines(relevant_files):
    total_lines = 0
    for file_path in relevant_files:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            total_lines += sum(1 for line in f)
    return total_lines


def count_lines_per_file_type(relevant_files):
    lines_per_type = collections.defaultdict(int)
    for file_path in relevant_files:
        _, ext = os.path.splitext(file_path)
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines_per_type[ext] += sum(1 for line in f)
    return dict(lines_per_type)


def count_files_per_type(relevant_files):
    files_per_type = collections.defaultdict(int)
    for file_path in relevant_files:
        _, ext = os.path.splitext(file_path)
        files_per_type[ext] += 1
    return dict(files_per_type)


def calculate_average_file_size(relevant_files):
    total_size = sum(os.path.getsize(file_path)
                     for file_path in relevant_files)
    return total_size / len(relevant_files) if relevant_files else 0


def find_largest_file(relevant_files):
    largest_file = {'name': '', 'size': 0, 'lines': 0}
    for file_path in relevant_files:
        size = os.path.getsize(file_path)
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = sum(1 for line in f)
        if size > largest_file['size']:
            largest_file = {'name': os.path.basename(
                file_path), 'size': size, 'lines': lines}
    return largest_file


def calculate_statistics(repo_dir, folder_structure, gitignore):
    relevant_files = get_relevant_files(repo_dir, gitignore)
    stats = {}
    stats['total_files'] = len(relevant_files)
    stats['total_lines'] = count_total_lines(relevant_files)
    stats['lines_per_file_type'] = count_lines_per_file_type(relevant_files)
    stats['files_per_type'] = count_files_per_type(relevant_files)
    stats['average_file_size'] = calculate_average_file_size(relevant_files)
    stats['largest_file'] = find_largest_file(relevant_files)
    return stats


def format_statistics(stats):
    formatted_stats = [
        "Code Statistics:",
        f"1. Total number of files: {stats['total_files']}",
        f"2. Total lines of code: {stats['total_lines']}",
        "3. Lines of code per file type:",
    ]
    for ext, lines in stats['lines_per_file_type'].items():
        formatted_stats.append(f"   - {ext or 'No extension'}: {lines}")

    formatted_stats.extend([
        "4. Number of files per file type:",
    ])
    for ext, count in stats['files_per_type'].items():
        formatted_stats.append(f"   - {ext or 'No extension'}: {count}")

    formatted_stats.extend([
        f"5. Average file size: {stats['average_file_size']:.2f} bytes",
        "6. Largest file:",
        f"   - Name: {stats['largest_file']['name']}",
        f"   - Size: {stats['largest_file']['size']} bytes",
        f"   - Lines: {stats['largest_file']['lines']}",
    ])

    return "\n".join(formatted_stats)


# Parse the .gitignore file
gitignore_path = os.path.join(repo_dir, '.gitignore')
gitignore = parse_gitignore(gitignore_path)

if gitignore is None:
    print("No .gitignore file found. Proceeding without ignoring any files.")

# Get folder structure
folder_structure = list(get_folder_structure(repo_dir, gitignore, output_file))

# Calculate statistics
stats = calculate_statistics(repo_dir, folder_structure, gitignore)

with open(output_file, 'w', encoding='utf-8') as outfile:
    # Write statistics
    outfile.write(format_statistics(stats))
    outfile.write("\n\n")

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
