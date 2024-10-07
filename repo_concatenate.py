import os
import sys
from pathlib import Path
import re

# Configuration
CONFIG = {
    "REPO_DIR": ".",
    "OUTPUT_FILE_SUFFIX": ".txt",
    "GITIGNORE_FILENAME": ".gitignore",
    "MAX_LINES_FOR_TRUNCATED_FILES": 300,
    "BINARY_EXTENSIONS": {
        ".webp", ".jpg", ".jpeg", ".png", ".gif", ".pdf", ".zip", ".exe", ".ico", ".svg", ".pyc"
    },
    "IGNORE_FILES": {
        "package-lock.json", "yarn.lock", ".DS_Store", "Thumbs.db",
        ".gitattributes", ".eslintcache", ".npmrc", ".yarnrc"
    },
    "IGNORE_DIRS": {"__pycache__", ".git"},
    "TRUNCATE_EXTENSIONS": {".json", ".geojson"}
}

# Derived constants
REPO_NAME = Path(CONFIG["REPO_DIR"]).resolve().name
OUTPUT_FILE = f"{REPO_NAME}{CONFIG['OUTPUT_FILE_SUFFIX']}"
SCRIPT_NAME = Path(__file__).name

def handle_error(error_message, exit_program=False):
    """Print error message and optionally exit the program."""
    print(f"Error: {error_message}", file=sys.stderr)
    if exit_program:
        print("Exiting program due to error.", file=sys.stderr)
        sys.exit(1)

def parse_gitignore(file_path):
    """Parse .gitignore file and return a filter function."""
    try:
        if Path(file_path).exists():
            with open(file_path, 'r') as f:
                patterns = [line.strip() for line in f if line.strip() and not line.startswith('#')]

            def gitignore_filter(file):
                file_str = str(file)
                return any(re.match(re.escape(pattern).replace(r'\*', '.*').replace(r'\?', '.'), file_str) for pattern in patterns)

            return gitignore_filter
    except Exception as e:
        handle_error(f"Failed to parse .gitignore file: {e}")
    return None

def is_file_empty(file_path):
    """Check if a file is empty."""
    return Path(file_path).stat().st_size == 0

def should_include_file(file_path, gitignore, include_empty=False):
    """Determine if a file should be included in the output."""
    file_name = Path(file_path).name
    ext = Path(file_path).suffix.lower()
    return (
        file_name != OUTPUT_FILE
        and file_name != SCRIPT_NAME
        and file_name != CONFIG["GITIGNORE_FILENAME"]
        and file_name not in CONFIG["IGNORE_FILES"]
        and (gitignore is None or not gitignore(file_path))
        and (include_empty or not is_file_empty(file_path))
        and ext not in CONFIG["BINARY_EXTENSIONS"]
    )

def get_relevant_files(repo_dir, gitignore):
    """Get all relevant files in the repository."""
    relevant_files = []
    for root, dirs, files in os.walk(repo_dir):
        dirs[:] = [d for d in dirs if d not in CONFIG["IGNORE_DIRS"] and (gitignore is None or not gitignore(os.path.join(root, d)))]
        for file in files:
            full_path = Path(root) / file
            if should_include_file(full_path, gitignore):
                relevant_files.append(full_path)
    return relevant_files

def get_folder_structure(start_path, gitignore):
    """Generate a visual representation of the folder structure."""
    structure = [f"{REPO_NAME}/"]

    def add_to_structure(current_path, prefix=""):
        entries = sorted(current_path.iterdir(), key=lambda x: x.name)
        filtered_entries = [
            e for e in entries
            if e.name not in CONFIG["IGNORE_DIRS"]
            and e.name != OUTPUT_FILE
            and e.name != SCRIPT_NAME
            and e.name != CONFIG["GITIGNORE_FILENAME"]
            and e.name not in CONFIG["IGNORE_FILES"]
            and (gitignore is None or not gitignore(str(e)))
        ]

        for i, entry in enumerate(filtered_entries):
            is_last = i == len(filtered_entries) - 1
            if entry.is_dir():
                structure.append(f"{prefix}{'└── ' if is_last else '├── '}{entry.name}/")
                add_to_structure(entry, prefix + ("    " if is_last else "│   "))
            else:
                structure.append(f"{prefix}{'└── ' if is_last else '├── '}{entry.name}")

    add_to_structure(Path(start_path))
    return structure

def count_total_lines(relevant_files):
    """Count the total number of lines in all relevant files."""
    total_lines = 0
    for file in relevant_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                total_lines += sum(1 for _ in f)
        except Exception as e:
            handle_error(f"Error counting lines in {file}: {e}")
    return total_lines

def count_lines_per_file_type(relevant_files):
    """Count the number of lines for each file type."""
    lines_per_type = {}
    for file in relevant_files:
        ext = file.suffix
        try:
            with open(file, 'r', encoding='utf-8') as f:
                lines_per_type[ext] = lines_per_type.get(ext, 0) + sum(1 for _ in f)
        except Exception as e:
            handle_error(f"Error counting lines in {file}: {e}")
    return lines_per_type

def count_files_per_type(relevant_files):
    """Count the number of files for each file type."""
    return {ext: sum(1 for file in relevant_files if file.suffix == ext)
            for ext in set(file.suffix for file in relevant_files)}

def calculate_average_file_size(relevant_files):
    """Calculate the average file size of all relevant files."""
    total_size = sum(file.stat().st_size for file in relevant_files)
    return total_size / len(relevant_files) if relevant_files else 0

def find_largest_file(relevant_files):
    """Find the largest file in the repository."""
    largest_file = {"name": "", "size": 0, "lines": 0}
    for file in relevant_files:
        size = file.stat().st_size
        if size > largest_file["size"]:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    lines = sum(1 for _ in f)
                largest_file = {"name": file.name, "size": size, "lines": lines}
            except Exception as e:
                handle_error(f"Error processing largest file {file}: {e}")
    return largest_file

def calculate_statistics(repo_dir, gitignore):
    """Calculate various statistics about the repository."""
    relevant_files = get_relevant_files(repo_dir, gitignore)
    return {
        "total_files": len(relevant_files),
        "total_lines": count_total_lines(relevant_files),
        "lines_per_file_type": count_lines_per_file_type(relevant_files),
        "files_per_type": count_files_per_type(relevant_files),
        "average_file_size": calculate_average_file_size(relevant_files),
        "largest_file": find_largest_file(relevant_files)
    }

def format_statistics(stats):
    """Format the statistics into a human-readable string."""
    formatted_stats = [
        "Code Statistics:",
        f"1. Total number of files: {stats['total_files']}",
        f"2. Total lines of code: {stats['total_lines']}",
        "3. Lines of code per file type:"
    ]
    for ext, lines in stats['lines_per_file_type'].items():
        formatted_stats.append(f"   - {ext or 'No extension'}: {lines}")

    formatted_stats.append("4. Number of files per file type:")
    for ext, count in stats['files_per_type'].items():
        formatted_stats.append(f"   - {ext or 'No extension'}: {count}")

    formatted_stats.extend([
        f"5. Average file size: {stats['average_file_size']:.2f} bytes",
        "6. Largest file:",
        f"   - Name: {stats['largest_file']['name']}",
        f"   - Size: {stats['largest_file']['size']} bytes",
        f"   - Lines: {stats['largest_file']['lines']}"
    ])

    return "\n".join(formatted_stats)

def process_file_content(file_path):
    """Process the content of a file, truncating if necessary."""
    ext = file_path.suffix.lower()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if ext in CONFIG["TRUNCATE_EXTENSIONS"] and len(lines) > CONFIG["MAX_LINES_FOR_TRUNCATED_FILES"]:
            truncated_content = "".join(lines[:CONFIG["MAX_LINES_FOR_TRUNCATED_FILES"]])
            return truncated_content + f"\n\n(truncated to {CONFIG['MAX_LINES_FOR_TRUNCATED_FILES']} lines for brevity, total file length: {len(lines)} lines)"

        return "".join(lines)
    except Exception as e:
        handle_error(f"Error processing file {file_path}: {e}")
        return f"Error: Unable to process file content for {file_path}"

def generate_ai_instructions():
    """Generate AI instructions for the output file."""
    return """
AI INSTRUCTIONS:
When assisting with this project, please adhere to the following guidelines:

1. Always return the full, working file when editing code, ready for copy-paste.
2. Follow language-specific conventions and maintain consistent style.
3. Write clear, self-documenting code with concise comments for complex logic.
4. Implement proper error handling and logging.
5. Design modular, reusable code following SOLID principles.
6. Prioritize readability and maintainability over cleverness.
7. Use descriptive names for variables, functions, and classes.
8. Keep functions small and focused on a single responsibility.
9. Practice proper scoping and avoid global variables.
10. Apply appropriate design patterns to improve code structure.

Please keep these instructions in mind when providing assistance or generating code for this project.

"""

def generate_file_index(relevant_files):
    """Generate a file index for relevant files."""
    return "\n".join(f"{i+1}. {file.relative_to(CONFIG['REPO_DIR'])}" for i, file in enumerate(relevant_files))

def process_relevant_files(relevant_files):
    """Process all relevant files and generate the output content."""
    output = ""
    for i, file_path in enumerate(relevant_files):
        rel_path = file_path.relative_to(CONFIG["REPO_DIR"])
        try:
            content = process_file_content(file_path)
            separator = "=" * 80 + "\n"
            file_header = f"FILE_{i+1:04d}: {rel_path}\n"
            output += f"\n{separator}{file_header}{separator}\n"
            output += content
            output += f"\n{separator}END OF FILE_{i+1:04d}: {rel_path}\n{separator}\n"
        except Exception as e:
            handle_error(f"Error while processing {file_path}: {e}")
    return output

def main():
    """Main function to orchestrate the entire process."""
    try:
        gitignore_path = Path(CONFIG["REPO_DIR"]) / CONFIG["GITIGNORE_FILENAME"]
        gitignore = parse_gitignore(gitignore_path)

        if gitignore is None:
            print(f"No {CONFIG['GITIGNORE_FILENAME']} file found. Proceeding without ignoring any files.")

        folder_structure = get_folder_structure(CONFIG["REPO_DIR"], gitignore)
        repository_statistics = calculate_statistics(CONFIG["REPO_DIR"], gitignore)

        output = generate_ai_instructions()
        output += "=" * 80 + "\n\n"
        output += format_statistics(repository_statistics)
        output += "\n\nFolder Structure:\n"
        output += "\n".join(folder_structure)
        output += "\n\nFile Index:\n"

        relevant_files = get_relevant_files(CONFIG["REPO_DIR"], gitignore)
        output += generate_file_index(relevant_files)
        output += "\n\n"

        output += process_relevant_files(relevant_files)

        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"All files have been concatenated into {OUTPUT_FILE}")

    except Exception as e:
        handle_error(f"An unexpected error occurred: {e}", exit_program=True)

if __name__ == "__main__":
    main()