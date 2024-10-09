# Repo Concatenator

Supercharge your LLM interactions with full repository context.

## What it does

Repo Concatenator creates a single file containing your entire codebase, making it easy to feed your project's context into Large Language Models (LLMs) like GPT-4.

## Key Features

- Respects `.gitignore` rules
- Handles binary files and empties
- Smart truncation for large files (e.g., JSON)
- Works with Python and JavaScript
- Customizable to fit your workflow

## Quick Start

### Python

```bash
wget https://raw.githubusercontent.com/gundurraga/repo-concatenate/main/repo_concatenate.py
python repo_concatenate.py
```

### JavaScript

```bash
wget https://raw.githubusercontent.com/gundurraga/repo-concatenate/main/repo_concatenate.js
npm install fs path url
node repo_concatenate.js
```

Your consolidated codebase will be saved as `{repo_name}.txt` in the current directory.

## Output

1. AI-friendly instructions
2. Repo stats
3. Folder structure
4. File index
5. Full file contents (with handy navigation headers)

## Why use Repo Concatenator?

- **LLM-optimized**: Perfect for providing full context to AI coding assistants
- **Time-saver**: No more copy-pasting multiple files
- **Flexible**: Customizable for various project types and sizes
- **Lightweight**: No complex dependencies or setups

## Contribute

Got ideas? Found a bug? Contributions are welcome! Open an issue or send a pull request on our [GitHub repository](https://github.com/gundurraga/repo-concatenate).

## License

MIT License. Go wild, just give credit where it's due. See the [LICENSE](https://github.com/gundurraga/repo-concatenate/blob/main/LICENSE) file for details.
