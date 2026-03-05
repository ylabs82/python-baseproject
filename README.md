# Python Base Project

A modern, opinionated command-line application template for building Python 3 CLI tools with Poetry.

This project template provides a solid foundation for creating Python CLI applications. It includes a modular structure for argument parsing, logging, error handling, and executable deployment ready for distribution via `pip` or Poetry.

---

## Technical Overview

### Project Structure

```
src/baseproject/
├── baseproject.py          # Main entry point and CLI logic
├── __init__.py             # Package initialization
└── base/
    ├── __init__.py         # Base package exports
    ├── arguments.py        # Argument parsing with argparse
    ├── consts.py           # Shared constants and configuration
    ├── helpers.py          # Utility functions (overwrites, checks)
    └── help.py             # Help messages and documentation
```

### Key Components

| Component | Purpose | File |
|-----------|---------|------|
| **CLI Module** | Defines program entry point, orchestrates workflow | `baseproject.py` |
| **Arguments Parser** | Handles CLI arguments, validation, and help output | `arguments.py` |
| **Constants** | Shared configuration (version, company, required commands) | `consts.py` |
| **Helpers** | Utility functions (file existence, overwrite confirmation) | `helpers.py` |
| **Help System** | Custom help messages and documentation | `help.py` |

### Dependencies

- **Python**: Requires Python 3.12+
- **Poetry**: Used for dependency and package management
- **Standard Library**: Built using `argparse`, `logging`, and OS modules only

### Installation & Usage

```bash
# Install project dependencies
poetry install

# Run as a module
poetry run baseproject --input=file.txt --output=result.txt --verbose

# Install globally as a CLI tool
poetry build
cd dist
pip install baseproject-*.tar.gz

# Run globally after installation
baseproject --input=file.txt --output=result.txt
```

### Project Features

**Built-in CLI Utilities**:
- ✅ Modular argument handling with `argparse`
- ✅ Validation of input/output files
- ✅ Confirm overwrite warnings
- ✅ Required system command checking
- ✅ Conditional logging verbosity (`--verbose` flag)
- ✅ Comprehensive help (`--help` and `--help <category>`)

**Structured Error Handling**:
- Graceful error messages with context
- Early exit strategies for invalid states
- Consistent error reporting via `sys.exit(code)`

---

## Bootstrapping a New Project

Instead of manually updating metadata and constants, use the `bootstrap_project.py` script to clone this template into a new project.

### 1. Running the Script

Execute the script from the repository root:

```bash
python3 bootstrap_project.py <project_name> <project_location>
```

**Positional arguments (required)**:
- `project_name` - Name of the new project (e.g., `my-tool`)
- `project_location` - Directory path to create the project (e.g., `./my-tool`)

**Optional flags**:
- `-h, --help` - Show help message and exit
- `-a, --auto` - Disable interactive prompts, run automatically with defaults
- `-i, --interactive` - Force interactive prompting mode (interactive by default)
- `--help-command` - Show additional command-line help

### 2. Usage Modes

**Interactive mode** (default):
The script will prompt you for:
1. Project name (default: `my-project`)
2. Project location (default: `./my-project`)
3. Author name
4. Author email
5. Program name
6. Company name

**Auto mode**:
```bash
python3 bootstrap_project.py my-tool ./my-tool -a
```

With `--auto`, the script uses default placeholder values and skips all prompts.

### 3. What the Script Does

The bootstrap script copies this template to a new location and replaces metadata:

**Creates**:
- New directory at the specified location
- `pyproject.toml` with project name, version, description, author, and company
- Package structure with updated metadata in `consts.py` and `help.py`
- Full `.git` repository initialized

**Replaces**:
- `"Python Base Project"` → `program_name` (user program name)
- `...` in "Original author" → `author_name <author_email>`
- `YYYY` → `PROG_YEAR`
- `...` in author field → `author_name`
- `author@email.com` → `author_email`

**Cleanup**:
- Deletes the source `bootstrap_project.py` from the new project
- Leaves `poetry.lock` (do not delete it)

### 4. After Bootstrapping

The script creates a completely new, self-contained project:

```bash
cd my-tool
poetry install
poetry run my-tool --help
```

Then customize:
1. **Business logic**: Edit `src/my_tool/my_tool.py` to add your implementation
2. **CLI arguments**: Adjust `arguments.py` as needed
3. **Help messages**: Update `help.py` with your own messages and documentation 
4. **Tests**: Update the `tests/` directory with your test cases
5. **Metadata**: Update `pyproject.toml` version or dependencies

### 5. Example Usage

Interactive example:
```bash
python3 bootstrap_project.py data-processor ./data-processor
# You'll be prompted for author, program name, company, etc.
```

Auto mode example:
```bash
python3 bootstrap_project.py analytics-cli ./analytics-cli -a
```

This generates a ready-to-use project structure following the same architecture and best practices as this template.

---

## Best Practices Used in This Template

- **Separation of Concerns**: Each component (arguments, helpers, constants) is isolated.
- **Early Exit Pattern**: Invalid states handled before business logic begins.
- **Logging with Levels**: `DEBUG`/`WARNING` verbosity control for better UX.
- **Cross-platform Support**: Uses `os.path`, `shutil.which()`, and standard library.
- **Self-documenting via CLI**: Comprehensive help output built-in.

---

## Development Workflow

1. Build package with `poetry build`
2. Run locally without installation: `poetry run baseproject --input test.txt --output out.txt`

---

## License

Add your preferred license (MIT, Apache 2.0, GPL, etc.) to the root or project repository settings.

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Run tests: `poetry run pytest`
4. Commit with conventional messages: `git commit -m "feat: add new feature"`
5. Push and open a pull request

---

## Acknowledgments

This template uses Poetry for dependency management and follows PEP specifications for Python packaging and command-line interface conventions.
