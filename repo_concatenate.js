import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import process from "node:process";

// Configuration
const CONFIG = {
  // Directory of the repository to process (current directory by default)
  REPO_DIR: ".",
  // Suffix for the output file
  OUTPUT_FILE_SUFFIX: ".txt",
  // Name of the gitignore file
  GITIGNORE_FILENAME: ".gitignore",
  // Maximum number of lines for truncated files
  MAX_LINES_FOR_TRUNCATED_FILES: 300,
  // File extensions to skip (binary files)
  BINARY_EXTENSIONS: [
    ".webp",
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".pdf",
    ".zip",
    ".exe",
    ".ico",
    ".svg",
  ],
  // Files to ignore
  IGNORE_FILES: [
    "package-lock.json",
    "yarn.lock",
    ".DS_Store",
    "Thumbs.db",
    ".gitattributes",
    ".eslintcache",
    ".npmrc",
    ".yarnrc",
  ],
  // File extensions to truncate
  TRUNCATE_EXTENSIONS: [".json", ".geojson"],
};

// Derived constants
const REPO_NAME = path.basename(path.resolve(CONFIG.REPO_DIR));
const OUTPUT_FILE = `${REPO_NAME}${CONFIG.OUTPUT_FILE_SUFFIX}`;
const SCRIPT_NAME = path.basename(fileURLToPath(import.meta.url));

// Convert arrays to sets for faster lookup
const BINARY_EXTENSIONS = new Set(CONFIG.BINARY_EXTENSIONS);
const IGNORE_FILES = new Set(CONFIG.IGNORE_FILES);
const TRUNCATE_EXTENSIONS = new Set(CONFIG.TRUNCATE_EXTENSIONS);

// Handle errors and optionally exit the program
function handleError(errorMessage, exitProgram = false) {
  console.error(`Error: ${errorMessage}`);
  if (exitProgram) {
    console.error("Exiting program due to error.");
    process.exit(1);
  }
}

// Parse the .gitignore file and return a function to check if a file should be ignored
function parseGitignore(filePath) {
  try {
    if (fs.existsSync(filePath)) {
      const gitignoreContent = fs.readFileSync(filePath, "utf8");
      const patterns = gitignoreContent
        .split("\n")
        .filter((line) => line.trim() !== "" && !line.startsWith("#"));
      return (file) =>
        patterns.some((pattern) => {
          const regexPattern = pattern
            .replace(/\./g, "\\.")
            .replace(/\*/g, ".*")
            .replace(/\?/g, ".");
          return new RegExp(regexPattern).test(file);
        });
    }
  } catch (e) {
    handleError(`Failed to parse .gitignore file: ${e}`);
  }
  return null;
}

// Check if a file is empty
function isFileEmpty(filePath) {
  return fs.statSync(filePath).size === 0;
}

// Determine if a file should be included in the output
function shouldIncludeFile(filePath, gitignore, includeEmpty = false) {
  const fileName = path.basename(filePath);
  const ext = path.extname(filePath).toLowerCase();
  return (
    fileName !== OUTPUT_FILE &&
    fileName !== SCRIPT_NAME &&
    fileName !== CONFIG.GITIGNORE_FILENAME &&
    !IGNORE_FILES.has(fileName) &&
    (gitignore === null || !gitignore(filePath)) &&
    (includeEmpty || !isFileEmpty(filePath)) &&
    !BINARY_EXTENSIONS.has(ext)
  );
}

// Get all relevant files in the repository
async function getRelevantFiles(repoDir, gitignore) {
  const relevantFiles = [];
  async function walk(dir) {
    const entries = await fs.promises.readdir(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        if (entry.name !== ".git" && (!gitignore || !gitignore(fullPath))) {
          await walk(fullPath);
        }
      } else if (shouldIncludeFile(fullPath, gitignore)) {
        relevantFiles.push(fullPath);
      }
    }
  }
  try {
    await walk(repoDir);
  } catch (e) {
    handleError(`Error while getting relevant files: ${e}`);
  }
  return relevantFiles;
}

// Generate a visual representation of the folder structure
async function getFolderStructure(startPath, gitignore) {
  const structure = [`${REPO_NAME}/`];
  async function addToStructure(currentPath, prefix = "") {
    try {
      const entries = await fs.promises.readdir(currentPath, {
        withFileTypes: true,
      });
      const filteredEntries = entries
        .filter(
          (e) =>
            e.name !== ".git" &&
            e.name !== OUTPUT_FILE &&
            e.name !== SCRIPT_NAME &&
            e.name !== CONFIG.GITIGNORE_FILENAME &&
            !IGNORE_FILES.has(e.name)
        )
        .filter((e) => !gitignore || !gitignore(path.join(currentPath, e.name)))
        .sort((a, b) => a.name.localeCompare(b.name));

      for (let i = 0; i < filteredEntries.length; i++) {
        const entry = filteredEntries[i];
        const isLast = i === filteredEntries.length - 1;
        if (entry.isDirectory()) {
          structure.push(`${prefix}${isLast ? "└── " : "├── "}${entry.name}/`);
          const extension = isLast ? "    " : "│   ";
          await addToStructure(
            path.join(currentPath, entry.name),
            prefix + extension
          );
        } else {
          structure.push(`${prefix}${isLast ? "└── " : "├── "}${entry.name}`);
        }
      }
    } catch (e) {
      handleError(`Error while generating folder structure: ${e}`);
    }
  }
  await addToStructure(startPath);
  return structure;
}

// Count the total number of lines in all relevant files
async function countTotalLines(relevantFiles) {
  let totalLines = 0;
  for (const filePath of relevantFiles) {
    try {
      const content = await fs.promises.readFile(filePath, "utf8");
      totalLines += content.split("\n").length;
    } catch (e) {
      handleError(`Error while counting lines in ${filePath}: ${e}`);
    }
  }
  return totalLines;
}

// Count the number of lines for each file type
async function countLinesPerFileType(relevantFiles) {
  const linesPerType = {};
  for (const filePath of relevantFiles) {
    try {
      const ext = path.extname(filePath);
      const content = await fs.promises.readFile(filePath, "utf8");
      linesPerType[ext] = (linesPerType[ext] || 0) + content.split("\n").length;
    } catch (e) {
      handleError(`Error while counting lines in ${filePath}: ${e}`);
    }
  }
  return linesPerType;
}

// Count the number of files for each file type
function countFilesPerType(relevantFiles) {
  return relevantFiles.reduce((acc, filePath) => {
    const ext = path.extname(filePath);
    acc[ext] = (acc[ext] || 0) + 1;
    return acc;
  }, {});
}

// Calculate the average file size of all relevant files
async function calculateAverageFileSize(relevantFiles) {
  try {
    const totalSize = await relevantFiles.reduce(
      async (accPromise, filePath) => {
        const acc = await accPromise;
        const stats = await fs.promises.stat(filePath);
        return acc + stats.size;
      },
      Promise.resolve(0)
    );
    return relevantFiles.length ? totalSize / relevantFiles.length : 0;
  } catch (e) {
    handleError(`Error while calculating average file size: ${e}`);
    return 0;
  }
}

// Find the largest file in the repository
async function findLargestFile(relevantFiles) {
  let largestFile = { name: "", size: 0, lines: 0 };
  for (const filePath of relevantFiles) {
    try {
      const stats = await fs.promises.stat(filePath);
      if (stats.size > largestFile.size) {
        const content = await fs.promises.readFile(filePath, "utf8");
        largestFile = {
          name: path.basename(filePath),
          size: stats.size,
          lines: content.split("\n").length,
        };
      }
    } catch (e) {
      handleError(`Error while processing ${filePath}: ${e}`);
    }
  }
  return largestFile;
}

// Calculate various statistics about the repository
async function calculateStatistics(repoDir, gitignore) {
  const relevantFiles = await getRelevantFiles(repoDir, gitignore);
  return {
    total_files: relevantFiles.length,
    total_lines: await countTotalLines(relevantFiles),
    lines_per_file_type: await countLinesPerFileType(relevantFiles),
    files_per_type: countFilesPerType(relevantFiles),
    average_file_size: await calculateAverageFileSize(relevantFiles),
    largest_file: await findLargestFile(relevantFiles),
  };
}

// Format the statistics into a human-readable string
function formatStatistics(stats) {
  const formattedStats = [
    "Code Statistics:",
    `1. Total number of files: ${stats.total_files}`,
    `2. Total lines of code: ${stats.total_lines}`,
    "3. Lines of code per file type:",
  ];
  for (const [ext, lines] of Object.entries(stats.lines_per_file_type)) {
    formattedStats.push(`   - ${ext || "No extension"}: ${lines}`);
  }

  formattedStats.push("4. Number of files per file type:");
  for (const [ext, count] of Object.entries(stats.files_per_type)) {
    formattedStats.push(`   - ${ext || "No extension"}: ${count}`);
  }

  formattedStats.push(
    `5. Average file size: ${stats.average_file_size.toFixed(2)} bytes`,
    "6. Largest file:",
    `   - Name: ${stats.largest_file.name}`,
    `   - Size: ${stats.largest_file.size} bytes`,
    `   - Lines: ${stats.largest_file.lines}`
  );

  return formattedStats.join("\n");
}

// Process the content of a file, truncating if necessary
async function processFileContent(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const content = await fs.promises.readFile(filePath, "utf8");
  const lines = content.split("\n");

  if (
    TRUNCATE_EXTENSIONS.has(ext) &&
    lines.length > CONFIG.MAX_LINES_FOR_TRUNCATED_FILES
  ) {
    const truncatedContent = lines
      .slice(0, CONFIG.MAX_LINES_FOR_TRUNCATED_FILES)
      .join("\n");
    return (
      truncatedContent +
      `\n\n(truncated to ${CONFIG.MAX_LINES_FOR_TRUNCATED_FILES} lines for brevity, total file length: ${lines.length} lines)`
    );
  }

  return content;
}

// Main function to orchestrate the entire process
async function main() {
  try {
    const gitignorePath = path.join(CONFIG.REPO_DIR, CONFIG.GITIGNORE_FILENAME);
    const gitignore = parseGitignore(gitignorePath);

    if (gitignore === null) {
      console.log(
        `No ${CONFIG.GITIGNORE_FILENAME} file found. Proceeding without ignoring any files.`
      );
    }

    const folderStructure = await getFolderStructure(
      CONFIG.REPO_DIR,
      gitignore
    );
    const repositoryStatistics = await calculateStatistics(
      CONFIG.REPO_DIR,
      gitignore
    );

    let output = generateAIInstructions();
    output += "=".repeat(80) + "\n\n";
    output += formatStatistics(repositoryStatistics);
    output += "\n\nFolder Structure:\n";
    output += folderStructure.join("\n");
    output += "\n\nFile Index:\n";

    const relevantFiles = await getRelevantFiles(CONFIG.REPO_DIR, gitignore);
    const fileIndex = generateFileIndex(relevantFiles);
    output += fileIndex;
    output += "\n\n";

    output += await processRelevantFiles(relevantFiles);

    await fs.promises.writeFile(OUTPUT_FILE, output, "utf8");
    console.log(`All files have been concatenated into ${OUTPUT_FILE}`);
  } catch (e) {
    handleError(`An unexpected error occurred: ${e}`, true);
  }
}

// Generate AI instructions for the output file
function generateAIInstructions() {
  return `AI INSTRUCTIONS:
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

`;
}

// Generate a file index for relevant files
function generateFileIndex(relevantFiles) {
  return relevantFiles
    .map(
      (file, index) => `${index + 1}. ${path.relative(CONFIG.REPO_DIR, file)}`
    )
    .join("\n");
}

// Process all relevant files and generate the output content
async function processRelevantFiles(relevantFiles) {
  let output = "";
  for (let i = 0; i < relevantFiles.length; i++) {
    const filePath = relevantFiles[i];
    const relPath = path.relative(CONFIG.REPO_DIR, filePath);
    try {
      const content = await processFileContent(filePath);
      const separator = "=".repeat(80) + "\n";
      const fileHeader = `FILE_${(i + 1)
        .toString()
        .padStart(4, "0")}: ${relPath}\n`;
      output += `\n${separator}${fileHeader}${separator}\n`;
      output += content;
      output += `\n${separator}END OF FILE_${(i + 1)
        .toString()
        .padStart(4, "0")}: ${relPath}\n${separator}\n`;
    } catch (e) {
      handleError(`Error while processing ${filePath}: ${e}`);
    }
  }
  return output;
}

main();
