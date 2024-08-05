# Repo Concatenator

## Overview

`repo_concatenate.py` is a Python script that combines all files in a GitHub repository (or any directory) into a single file, respecting `.gitignore` rules. It's designed to create a comprehensive view of your project's codebase, which can be incredibly useful for various purposes:

- **LLM Integration**: Easily feed your entire codebase to Large Language Models (LLMs) for analysis, code review, or to provide context for code-related queries.
- **Code Analysis**: Get a holistic view of your project, making it easier to understand the overall structure and interdependencies.
- **Documentation**: Generate a complete snapshot of your codebase for documentation purposes.
- **Code Sharing**: Simplify the process of sharing your entire codebase with others, such as for code reviews or collaboration.
- **Project Overviews**: Quickly create project summaries or overviews for stakeholders or new team members.

By concatenating all files into a single document, you can leverage powerful tools like LLMs to gain insights, generate documentation, or even get suggestions for improvements across your entire project.

## Features

- Concatenates all files in a directory into one file
- Respects `.gitignore` rules to exclude unnecessary files
- Adds clear section headers for each file in the output
- Simplifies the process of feeding project data to LLMs or other analysis tools

## Quick Start

1. **Download the script:**
   Place `repo_concatenate.py` in the root directory of the repository or folder you want to concatenate.

2. **Install the required dependency:**

   ```
   pip install gitignore-parser
   ```

3. **Run the script:**

   ```
   python repo_concatenate.py
   ```

   The concatenated output will be saved as `all_files_concatenated.txt` in the same directory.

## Customization (Optional)

If you want to change the default behavior:

- To specify a different output file name, modify the `output_file` variable in the script.
- To process a different directory, change the `repo_dir` variable.
- To use a different `.gitignore` file, update the `gitignore_path` variable.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request if you have ideas for improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
