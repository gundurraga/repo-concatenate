# Repo Concatenator

## Overview

Repo Concatenator is a tool available in both Python and JavaScript that combines all files in a GitHub repository (or any directory) into a single file, respecting `.gitignore` rules. It's designed to create a comprehensive view of your project's codebase, which is particularly useful for providing full context knowledge of a repo or folder to AI agents or Large Language Models (LLMs).

## Features

- Generates a tree-like folder structure of the project
- Creates a numbered file index
- Concatenates all files in the repository into a single file
- Respects `.gitignore` rules to exclude unnecessary files
- Adds clear section headers for each file in the output
- Excludes the output file itself and the script from the generated content
- Calculates and includes various statistics about the repository
- Implements error handling for improved reliability
- Available in both Python and JavaScript (Node.js) versions

## Primary Use Case

The principal use of Repo Concatenator is to provide full context knowledge of a repository or folder to a Large Language Model (LLM). This comprehensive view allows the LLM to understand the entire project structure, code relationships, and overall architecture, enabling more accurate and context-aware responses.

## Quick Start

### Python Version

1. **Download the script:**
   Place `repo_concatenate.py` in the root directory of the repository or folder you want to concatenate.

2. **Run the script:**
   ```
   python repo_concatenate.py
   ```

### JavaScript Version

1. **Download the script:**
   Place `repo-concatenate.js` in the root directory of the repository or folder you want to concatenate.

2. **Install dependencies:**

   ```
   npm install fs path url
   ```

3. **Run the script:**
   ```
   node repo-concatenate.js
   ```

For both versions, the concatenated output will be saved as `{repo_name}.txt` in the same directory.

## Output Format

The generated file includes:

1. AI instructions for working with the project
2. Repository statistics (file counts, line counts, etc.)
3. A tree-like folder structure of the project
4. A numbered index of all files
5. The full content of each file, clearly separated and numbered

This format allows for easy navigation and reference when working with AI tools or LLMs.

## Roadmap

We're constantly looking to improve Repo Concatenator to enhance its capabilities in assisting LLMs to write high-quality, best-practice code. Here are some key areas we're focusing on for future releases:

1. **Comprehensive Code Analysis**: Implement advanced code analysis features to provide LLMs with deeper insights into code quality, complexity, and adherence to best practices across various programming languages.

2. **Intelligent Context Generation**: Develop algorithms to generate more nuanced and informative context about the codebase, including identification of design patterns, architectural structures, and key dependencies.

3. **Customizable Quality Metrics**: Create a flexible system for defining and measuring code quality metrics tailored to specific project requirements, enabling LLMs to generate code that aligns more closely with user-defined standards and best practices.

These enhancements aim to provide LLMs with richer context and guidance to generate high-quality, best-practice code that aligns with the user's requirements and project standards.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request if you have ideas for improvements or new features that could enhance the tool's usefulness for AI and LLM applications.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
