import os
from collections import defaultdict

import gitignore_parser

# Configuration
# Directory containing the repository (current directory by default)
REPO_DIR = '.'
OUTPUT_FILE_SUFFIX = '.txt'  # Suffix for the output file
GITIGNORE_FILENAME = '.gitignore'

# Derived constants
REPO_NAME = os.path.basename(os.path.abspath(REPO_DIR))
OUTPUT_FILE = f'{REPO_NAME}{OUTPUT_FILE_SUFFIX}'
SCRIPT_NAME = os.path.basename(__file__)


def handle_error(error_message, exit_program=False):
    """
    Handle errors by printing the error message and optionally exiting the program.

    Args:
        error_message (str): The error message to display.
        exit_program (bool): Whether to exit the program after displaying the error.
    """
    print(f"Error: {error_message}")
    if exit_program:
        print("Exiting program due to error.")
        exit(1)


def parse_gitignore(file_path):
    """
    Parse the .gitignore file if it exists.

    Args:
        file_path (str): Path to the .gitignore file.

    Returns:
        function or None: A function that checks if a file should be ignored, or None if .gitignore doesn't exist.
    """
    try:
        if os.path.exists(file_path):
            return gitignore_parser.parse_gitignore(file_path)
    except Exception as e:
        handle_error(f"Failed to parse .gitignore file: {e}")
    return None


def should_include_file(file_path, gitignore):
    """
    Check if a file should be included based on .gitignore rules.

    Args:
        file_path (str): Path to the file to check.
        gitignore (function or None): Function to check if a file should be ignored.

    Returns:
        bool: True if the file should be included, False otherwise.
    """
    return (file_path != OUTPUT_FILE and
            os.path.basename(file_path) != SCRIPT_NAME and
            os.path.basename(file_path) != GITIGNORE_FILENAME and
            (gitignore is None or not gitignore(file_path)))


def get_relevant_files(repo_dir, gitignore):
    """
    Get all relevant files respecting .gitignore rules.

    Args:
        repo_dir (str): Path to the repository directory.
        gitignore (function or None): Function to check if a file should be ignored.

    Returns:
        list: List of relevant file paths.
    """
    relevant_files = []
    try:
        for root, dirs, files in os.walk(repo_dir):
            if '.git' in dirs:
                dirs.remove('.git')
            if gitignore:
                dirs[:] = [d for d in dirs if not gitignore(
                    os.path.join(root, d))]
            for file in files:
                file_path = os.path.join(root, file)
                if should_include_file(file_path, gitignore):
                    relevant_files.append(file_path)
    except Exception as e:
        handle_error(f"Error while getting relevant files: {e}")
    return relevant_files


def get_folder_structure(start_path, gitignore):
    """
    Generate a tree-like folder structure respecting .gitignore rules.

    Args:
        start_path (str): Path to start generating the folder structure from.
        gitignore (function or None): Function to check if a file should be ignored.

    Yields:
        str: Lines representing the folder structure.
    """
    def add_to_structure(path, prefix=''):
        try:
            entries = sorted(os.scandir(path), key=lambda e: e.name)
            entries = [e for e in entries if e.name !=
                       '.git' and e.name != OUTPUT_FILE and e.name != SCRIPT_NAME and e.name != GITIGNORE_FILENAME]
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
        except Exception as e:
            handle_error(f"Error while generating folder structure: {e}")

    yield f"{REPO_NAME}/"
    yield from add_to_structure(start_path)


def count_total_lines(relevant_files):
    """
    Count total lines of code in all relevant files.

    Args:
        relevant_files (list): List of relevant file paths.

    Returns:
        int: Total number of lines in all relevant files.
    """
    total_lines = 0
    for file_path in relevant_files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                total_lines += sum(1 for _ in f)
        except Exception as e:
            handle_error(f"Error while counting lines in {file_path}: {e}")
    return total_lines


def count_lines_per_file_type(relevant_files):
    """
    Count lines of code per file type.

    Args:
        relevant_files (list): List of relevant file paths.

    Returns:
        dict: Dictionary with file extensions as keys and line counts as values.
    """
    lines_per_type = defaultdict(int)
    for file_path in relevant_files:
        try:
            _, ext = os.path.splitext(file_path)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines_per_type[ext] += sum(1 for _ in f)
        except Exception as e:
            handle_error(f"Error while counting lines in {file_path}: {e}")
    return dict(lines_per_type)


def count_files_per_type(relevant_files):
    """
    Count number of files per file type.

    Args:
        relevant_files (list): List of relevant file paths.

    Returns:
        dict: Dictionary with file extensions as keys and file counts as values.
    """
    files_per_type = defaultdict(int)
    for file_path in relevant_files:
        _, ext = os.path.splitext(file_path)
        files_per_type[ext] += 1
    return dict(files_per_type)


def calculate_average_file_size(relevant_files):
    """
    Calculate the average file size of relevant files.

    Args:
        relevant_files (list): List of relevant file paths.

    Returns:
        float: Average file size in bytes.
    """
    try:
        total_size = sum(os.path.getsize(file_path)
                         for file_path in relevant_files)
        return total_size / len(relevant_files) if relevant_files else 0
    except Exception as e:
        handle_error(f"Error while calculating average file size: {e}")
        return 0


def find_largest_file(relevant_files):
    """
    Find the largest file among relevant files.

    Args:
        relevant_files (list): List of relevant file paths.

    Returns:
        dict: Dictionary containing information about the largest file.
    """
    largest_file = {'name': '', 'size': 0, 'lines': 0}
    for file_path in relevant_files:
        try:
            size = os.path.getsize(file_path)
            if size > largest_file['size']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = sum(1 for _ in f)
                largest_file = {
                    'name': os.path.basename(file_path),
                    'size': size,
                    'lines': lines
                }
        except Exception as e:
            handle_error(f"Error while processing {file_path}: {e}")
    return largest_file


def calculate_statistics(repo_dir, gitignore):
    """
    Calculate various statistics about the repository.

    Args:
        repo_dir (str): Path to the repository directory.
        gitignore (function or None): Function to check if a file should be ignored.

    Returns:
        dict: Dictionary containing various statistics about the repository.
    """
    relevant_files = get_relevant_files(repo_dir, gitignore)
    return {
        'total_files': len(relevant_files),
        'total_lines': count_total_lines(relevant_files),
        'lines_per_file_type': count_lines_per_file_type(relevant_files),
        'files_per_type': count_files_per_type(relevant_files),
        'average_file_size': calculate_average_file_size(relevant_files),
        'largest_file': find_largest_file(relevant_files)
    }


def format_statistics(stats):
    """
    Format the calculated statistics into a readable string.

    Args:
        stats (dict): Dictionary containing various statistics about the repository.

    Returns:
        str: Formatted string of statistics.
    """
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


def main():
    """Main function to run the script."""
    try:
        gitignore_path = os.path.join(REPO_DIR, GITIGNORE_FILENAME)
        gitignore = parse_gitignore(gitignore_path)

        if gitignore is None:
            print(
                f"No {GITIGNORE_FILENAME} file found. Proceeding without ignoring any files.")

        folder_structure = list(get_folder_structure(REPO_DIR, gitignore))
        stats = calculate_statistics(REPO_DIR, gitignore)

        with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
            outfile.write(format_statistics(stats))
            outfile.write("\n\nFolder Structure:\n")
            outfile.write("\n".join(folder_structure))
            outfile.write("\n\nFile Index:\n")

            file_index = []
            file_number = 1

            for root, dirs, files in os.walk(REPO_DIR):
                if '.git' in dirs:
                    dirs.remove('.git')
                if gitignore:
                    dirs[:] = [d for d in dirs if not gitignore(
                        os.path.join(root, d))]
                for file in files:
                    file_path = os.path.join(root, file)
                    if should_include_file(file_path, gitignore):
                        rel_path = os.path.relpath(file_path, REPO_DIR)
                        file_index.append(f"{file_number}. {rel_path}")
                        file_number += 1

            outfile.write("\n".join(file_index))
            outfile.write("\n\n")

            file_number = 1

            for root, dirs, files in os.walk(REPO_DIR):
                if '.git' in dirs:
                    dirs.remove('.git')
                if gitignore:
                    dirs[:] = [d for d in dirs if not gitignore(
                        os.path.join(root, d))]
                for file in files:
                    file_path = os.path.join(root, file)
                    if should_include_file(file_path, gitignore):
                        rel_path = os.path.relpath(file_path, REPO_DIR)
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                                separator = f"{'=' * 80}\n"
                                file_header = f"FILE_{file_number:04d}: {rel_path}\n"
                                outfile.write(
                                    f"\n{separator}{file_header}{separator}\n")
                                outfile.write(infile.read())
                                outfile.write(
                                    f"\n{separator}END OF FILE_{file_number:04d}: {rel_path}\n{separator}\n")
                                file_number += 1
                        except Exception as e:
                            handle_error(
                                f"Error while processing {file_path}: {e}")

        print(f"All files have been concatenated into {OUTPUT_FILE}")
    except Exception as e:
        handle_error(f"An unexpected error occurred: {e}", exit_program=True)


if __name__ == "__main__":
    main()
