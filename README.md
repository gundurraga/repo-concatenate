# Repo Concatenator

## Overview

Repo Concatenator is a Python script that combines all files in a GitHub repository (or any directory) into a single file, respecting `.gitignore` rules. It's designed to create a comprehensive view of your project's codebase, which is particularly useful for providing full context knowledge of a repo or folder to AI agents or Large Language Models (LLMs).

## Features

- Generates a tree-like folder structure of the project
- Creates a numbered file index
- Concatenates all files in the repository into a single file
- Respects `.gitignore` rules to exclude unnecessary files
- Adds clear section headers for each file in the output
- Excludes the output file itself and the script from the generated content
- Calculates and includes various statistics about the repository
- Implements error handling for improved reliability

## Primary Use Case

The principal use of Repo Concatenator is to provide full context knowledge of a repository or folder to a Large Language Model (LLM). This comprehensive view allows the LLM to understand the entire project structure, code relationships, and overall architecture, enabling more accurate and context-aware responses.

## Quick Start

1. **Download the script:**
   Place `repo_concatenator.py` in the root directory of the repository or folder you want to concatenate.

2. **Install the required dependency:**

   ```
   pip install gitignore-parser
   ```

3. **Run the script:**

   ```
   python repo_concatenator.py
   ```

   The concatenated output will be saved as `{repo_name}.txt` in the same directory.

## Output Format

The generated file includes:

1. Repository statistics (file counts, line counts, etc.)
2. A tree-like folder structure of the project
3. A numbered index of all files
4. The full content of each file, clearly separated and numbered

This format allows for easy navigation and reference when working with AI tools or LLMs.

## Roadmap

We're constantly looking to improve Repo Concatenator. Here are some features we're considering for future releases:

1. **Multi-language support**: Develop versions of the script in other programming languages (e.g., Javascript, Ruby) for broader accessibility.
2. **Incremental updates**: Implement a feature to update the output file only with changes since the last run, improving efficiency for large repositories.
3. **Advanced filtering options**: Provide more granular control over which files are included or excluded beyond .gitignore rules.
4. **Performance optimization**: Improve processing speed for very large repositories.

We welcome contributions and suggestions for new features that could enhance the tool's usefulness for AI and LLM applications.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request if you have ideas for improvements or new features that could enhance the tool's usefulness for AI and LLM applications.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
