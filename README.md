# Repo Concatenator

## Overview

Repo Concatenator is a Python script that combines all files in a GitHub repository (or any directory) into a single file, respecting `.gitignore` rules. It's designed to create a comprehensive view of your project's codebase, which is particularly useful for providing context to AI agents or Large Language Models (LLMs).

## Features

- Generates a tree-like folder structure of the project
- Creates a numbered file index
- Concatenates all files in the repository into a single file
- Respects `.gitignore` rules to exclude unnecessary files
- Adds clear section headers for each file in the output
- Excludes the output file itself and the script from the generated content

## Use Cases for AI and LLM Integration

- **Contextual Understanding**: Provide a complete project overview to AI agents or LLMs for more accurate and context-aware responses.
- **Code Analysis**: Enable AI tools to perform comprehensive code reviews or suggest improvements across the entire project.
- **Documentation Generation**: Use AI to generate or update project documentation based on the full codebase.
- **Architectural Insights**: Allow AI to analyze the project structure and suggest architectural improvements.
- **Dependency Analysis**: Help AI tools identify and analyze project dependencies more effectively.
- **Consistency Checking**: Enable AI to check for coding style consistency across the entire project.
- **Bug Detection**: Provide full context for AI-powered bug detection and resolution suggestions.
- **Feature Suggestion**: Allow AI to suggest new features or improvements based on a complete understanding of the existing codebase.

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

1. A tree-like folder structure of the project
2. A numbered index of all files
3. The full content of each file, clearly separated and numbered

This format allows for easy navigation and reference when working with AI tools or LLMs.

## Roadmap

We're constantly looking to improve Repo Concatenator. Here are some features we're considering for future releases:

1. **Code statistics**: Include basic code statistics like line counts, language breakdown, etc.
2. **Syntax highlighting**: Add optional syntax highlighting for code sections in the output.
3. **Metadata extraction**: Extract and summarize project metadata (e.g., dependencies, version numbers) for quick reference.

We welcome contributions and suggestions for new features that could enhance the tool's usefulness for AI and LLM applications.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request if you have ideas for improvements or new features that could enhance the tool's usefulness for AI and LLM applications.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
