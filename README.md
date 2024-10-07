# Repo Concatenator

A simple, agnostic tool to concatenate repository contents into a single file.

## Overview

Repo Concatenator combines all files in a repository or directory into one file, respecting `.gitignore` rules. It provides a comprehensive view of your project's codebase, useful for context-aware AI interactions.

## Features

- Generates project folder structure
- Creates a file index
- Concatenates files into a single output
- Respects `.gitignore` rules
- Adds file section headers
- Calculates basic repository statistics
- Available in Python and JavaScript

## Usage

### Python Version

1. Place `repo_concatenate.py` in your project's root directory.
2. Run: `python repo_concatenate.py`

### JavaScript Version

1. Place `repo-concatenate.js` in your project's root directory.
2. Install dependencies: `npm install fs path url`
3. Run: `node repo-concatenate.js`

Output is saved as `{repo_name}.txt` in the same directory.

## Output Format

1. AI instructions
2. Repository statistics
3. Folder structure
4. File index
5. Full content of each file

## Contributing

Contributions are welcome. Open an issue or submit a pull request for improvements or new features.

## License

MIT License. See LICENSE file for details.
