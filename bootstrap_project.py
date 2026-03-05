#!/usr/bin/env python3

"""Script to bootstrap a new Python CLI project from the base project template.

This script copies the template structure to a new location and replaces all
occurrences of the template's metadata with user-provided values.
"""

import argparse
import datetime
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Optional


VERSION = "1.0.0"
TEMPLATE_ROOT = Path(__file__).parent.resolve()


def snake_case(name: str) -> str:
    """Convert a string to snake_case format.

    Converts kebab-case and camelCase to snake_case.
    Handles numbers and consecutive uppercase letters.

    Args:
        name: The string to convert

    Returns:
        The converted name in snake_case format
    """
    # Handle camelCase
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    s2 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1)
    # Convert kebab-case to underscores and lowercase everything
    s3 = re.sub(r"[-]+", "_", s2)
    return s3.lower().strip("._")


def is_camel_case(name: str) -> bool:
    """Check if the name uses camelCase notation.

    Args:
        name: The string to check

    Returns:
        True if the name contains uppercase letters after the first character
        and is not all uppercase
    """
    return bool(re.search(r"[a-z][A-Z]", name))


def to_package_name(name: str) -> str:
    """Convert a project name to a valid Python package name.

    Args:
        name: The raw project name (e.g., "my-awesome-tool" or "MyProject")

    Returns:
        A valid Python package name in snake_case format
    """
    if name.isupper():
        return name.lower()
    return snake_case(name)


def read_file(path: Path) -> Optional[str]:
    """Read file contents and return as string.

    Args:
        path: Path to the file to read

    Returns:
        File contents as string, or None if not found
    """
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None


def write_file(path: Path, content: str) -> None:
    """Write content to file, ensuring parent directories exist.

    Args:
        path: Path to the file to write
        content: Content to write to the file
    """
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    except Exception as e:
        print(f"Error writing {path}: {e}", file=sys.stderr)
        raise


def process_file(
    file_path: Path,
    replacements: dict,
    current_year: str,
    author_name: str,
    author_email: str,
) -> None:
    """Process a single file, applying replacements and writing back if needed.

    Args:
        file_path: Path to the file to process
        replacements: Dictionary of old->new string replacements
        current_year: Current year as string
        author_name: Name of the author
        author_email: Email of the author
    """
    if not file_path.is_file():
        return

    content = read_file(file_path)
    if content is None:
        return

    try:
        content.encode("utf-8")
    except UnicodeDecodeError:
        return

    original = content

    # Replace project name variations
    for old, new in replacements.items():
        content = content.replace(old, new)

    # Update YYYY placeholder for copyright year with author info
    author_copyright = f"Copyright (c) {current_year}, {author_name} <{author_email}>"
    content = content.replace("Copyright (c) YYYY, ...", f"{author_copyright}")
    content = re.sub(
        r"\bYYYY\b",
        current_year,
        content
    )

    if content != original:
        write_file(file_path, content)


def copy_dir(src: Path, dst: Path) -> bool:
    """Copy directory recursively, creating dst if necessary.

    Args:
        src: Source directory path
        dst: Destination directory path

    Returns:
        True if successful, False otherwise
        Raises exception if source does not exist
    """
    if not src.exists():
        raise FileNotFoundError(f"Source directory not found: {src}")
    if dst.exists() and any(dst.iterdir()):
        print(f"Destination '{dst}' exists and is not empty, attempting to overwrite...")
        shutil.rmtree(dst)
    try:
        shutil.copytree(src, dst)
        print(f"  Copied: {src} -> {dst}")
        return True
    except Exception as e:
        print(f"FAILED to copy {src} to {dst}: {e}", file=sys.stderr)
        raise


def move_dir(src: Path, dst: Path) -> bool:
    """Rename/move the directory from src to dst.

    Args:
        src: Source directory path
        dst: Destination directory path

    Returns:
        True if successful, False otherwise
        Raises exception if source does not exist
    """
    if not src.exists():
        print(f"Warning: Source directory does not exist: {src}", file=sys.stderr)
        return False
    try:
        if dst.exists():
            print(f"Warning: Destination exists, removing: {dst}")
            shutil.rmtree(dst)
        src.rename(dst)
        print(f"  Renamed: {src} => {dst}")
        return True
    except Exception as e:
        print(f"FAILED to move {src} to {dst}: {e}", file=sys.stderr)
        raise


def is_valid_name(name: str) -> bool:
    """Check if the project name is valid.

    Valid names contain only alphanumeric characters, hyphens, and underscores.
    Must not be empty or start with a number.

    Args:
        name: The name to validate

    Returns:
        True if valid, False otherwise
    """
    if not name or len(name) > 100:
        return False
    if name[0].isdigit():
        return False
    return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9_-]*$", name))


def is_valid_email(email: str) -> bool:
    """Check if the provided email is valid.

    Args:
        email: Email address string to validate

    Returns:
        True if valid email format, False otherwise
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def process_toml_file(
        file_path: Path,
        new_package_name: str,
        project_name: str,
        author_name: str,
        author_email: str,
        current_year: str,
) -> None:
    """Special processing for pyproject.toml to handle author fields correctly.

    This function handles the pyproject.toml file specially because simple
    string replacement would corrupt the TOML structure by replacing 'author'
    text in other fields.

    Args:
        file_path: Path to the pyproject.toml file
        new_package_name: The new package name
        project_name: The user-friendly project name
        author_name: Name of the project author
        author_email: Email of the project author
        current_year: Current year for copyright
    """
    try:
        content = file_path.read_text(encoding='utf-8')

        # Replace the author line completely (not simple string replacement)
        # Find the line: {name = "author", email = "author@example.com"}
        old_author_line = '    {name = "author", email = "author@example.com"}'
        old_author_line_alternative = "    {name = 'author', email = 'author@example.com'}"

        if old_author_line in content:
            new_author_line = f'    {{name = "{author_name}", email = "{author_email}"}}'
            content = content.replace(old_author_line, new_author_line)
        elif old_author_line_alternative in content:
            new_author_line = f"    {{name = '{author_name}', email = '{author_email}'}}"
            content = content.replace(old_author_line_alternative, new_author_line)

        # Replace project name in description field
        old_description = '"A template for Python 3 command-line applications"'
        new_description = f'"{project_name} - {project_name} application"'
        if old_description in content:
            content = content.replace(old_description, new_description)

        # Replace copyright year placeholder
        old_copyright = 'Copyright (c) 2026.'
        new_copyright = f'Copyright (c) {current_year}.'
        if old_copyright in content:
            content = content.replace(old_copyright, new_copyright)

        # Replace version number
        if '"version = "0.0.0""' in content:
            content = content.replace('"version = "0.0.0""', '"version = "0.0.1""')
        else:
            content = content.replace('version = "0.0.0"', 'version = "0.0.1"')

        # Replace baseproject references with the actual package name
        content = content.replace('baseproject', new_package_name,
                                  content.count('baseproject') - content.count(f'{new_package_name}'))

        # Update the entry point script
        old_script = 'baseproject = "baseproject.baseproject:main"'
        new_script = f'{new_package_name} = "{new_package_name}.{new_package_name}:main"'
        if old_script in content:
            content = content.replace(old_script, new_script)

        # Update poetry packages section
        old_poetry_package = '{include = "baseproject", from = "src"}'
        new_poetry_package = f'{{include = "{new_package_name}", from = "src"}}'
        if old_poetry_package in content:
            content = content.replace(old_poetry_package, new_poetry_package)

        file_path.write_text(content, encoding='utf-8')

    except Exception as e:
        print(f"ERROR: Failed to process TOML file {file_path}: {e}", file=sys.stderr)
        raise


def prompt_string(
        prompt: str,
        default: str = "",
        required: bool = True
) -> str:
    """Prompt user for string input with optional default value.

    Args:
        prompt: The prompt message to display
        default: Default value if user presses Enter
        required: Whether the field must have a value

    Returns:
        The user's input as a string
    """
    default_text = f" [default={default}]" if default else ""
    while True:
        if default:
            value = input(f"{prompt}{default_text}: ").strip()
            return value if value else default
        value = input(f"{prompt}: ").strip()
        if value:
            return value
        if not required:
            return ""
        print("This field is required. Please try again.")


def prompt_project_name(current_name: Optional[str] = None) -> str | None:
    """Prompt user to provide a valid project name.

    Args:
        current_name: Pre-populated name from command line args (optional)

    Returns:
        A valid project name in lowercase or None if the provided name is invalid
    """
    while True:
        if not current_name:
            current_name = prompt_string(
                "Enter the new project name",
                default="my-project",
                required=True
            )

        if not is_valid_name(current_name):
            print("Invalid project name.")
            print("  Must start with a letter.")
            print("  Can contain lowercase letters, numbers, hyphens, and underscores.")
            print("  Example: my-awesome-tool or my_awesome_tool")
            current_name = None
            continue

        return current_name.lower()


def prompt_project_location(
    location: Optional[str] = None,
    root: Path = TEMPLATE_ROOT
) -> str | None:
    """Prompt user for a valid project location.

    Args:
        location: User-provided path, or None to prompt interactively
        root: The template root directory

    Returns:
        Absolute path to the new project directory
    """
    while True:
        if not location:
            location = prompt_string(
                "Enter the location for the new project",
                default="./my-project",
                required=True
            )

        project_path = Path(location).resolve()

        if project_path == root:
            print("Error: Cannot create project in the same directory as the template.")
            location = None
            continue

        if project_path.exists():
            if not project_path.is_dir():
                print("Error: Path exists but is not a directory.")
                location = None
                continue
            entries = list(project_path.iterdir())
            if entries:
                response = input(
                    f"Directory '{project_path}' already exists and is not empty.\n"
                    "Overwrite? [y/N]: "
                ).lower()
                if response != "y":
                    location = None
                    continue

        return str(project_path)


def get_user_info() -> tuple:
    """Prompt user for their name and email information.

    Returns:
        Tuple of (author_name, author_email, program_name, program_company)
    """
    author_name = prompt_string(
        "Enter your full name",
        default="Your Name",
        required=True
    )

    author_email = prompt_string(
        "Enter your email address",
        default="you@example.com",
        required=True
    )

    program_name = prompt_string(
        "Enter program name (description or name of your program)",
        default="My Custom Program",
        required=True
    )

    program_company = prompt_string(
        "Enter company/organization name (or your name if personal)",
        default="Company Name",
        required=True
    )

    print()

    return author_name, author_email, program_name, program_company


def bootstrap_project(
    project_name: str,
    location: str,
    author_name: str,
    author_email: str,
    program_name: str,
    program_company: str,
    keep_template: bool = False
) -> None:
    """Create a new project by copying and modifying template files.

    Args:
        project_name: Name of the new project (kebab-case or camelCase)
        location: Absolute path to create the new project
        author_name: Author name for metadata
        author_email: Author email for metadata
        program_name: Name of the user program (for consts.py PROG_NAME)
        program_company: Company/organization name (for consts.py PROG_COMPANY)
        keep_template: Whether to preserve the template after copying
    """
    print("\n" + "="*60)
    print("Bootstrap Project")
    print("="*60 + "\n")

    # Validate template exists before proceeding
    template_src = TEMPLATE_ROOT / "src"
    if not template_src.exists():
        print(f"ERROR: Template source directory not found: {template_src}", file=sys.stderr)
        print(f"Template root: {TEMPLATE_ROOT}", file=sys.stderr)
        print(f"Please ensure you are running this script from the project root.", file=sys.stderr)
        sys.exit(1)

    template_files = ["pyproject.toml", "README.md"]
    for file_name in template_files:
        template_file = TEMPLATE_ROOT / file_name
        if not template_file.exists():
            print(f"ERROR: Template file not found: {template_file}", file=sys.stderr)
            sys.exit(1)

    original_dir = os.getcwd()

    try:
        new_project_path = Path(location).resolve()
        src_dir = template_src
        new_package_name = to_package_name(project_name)

        print(f"Project Name: {project_name}")
        print(f"Package Name: {new_package_name}")
        print(f"Location: {new_project_path}")
        print(f"Author: {author_name} <{author_email}>")
        print(f"Program Name: {program_name}")
        print(f"Company: {program_company}")
        print(f"Template Root: {TEMPLATE_ROOT}")
        print()

        if not keep_template:
            answer = input("Copy template to new location? [y/N] ").lower()
            if answer != "y":
                print("Aborted by user.")
                return
        else:
            print("Proceeding with automated setup...")
            keep_template = False

        print()
        print("Step 1: Copying template files...")

        new_src_dir = new_project_path / "src"
        copy_dir(src_dir, new_src_dir)

        for file_name in ["pyproject.toml", "README.md"]:
            src_file = TEMPLATE_ROOT / file_name
            dst_file = new_project_path / file_name
            shutil.copy2(src_file, dst_file)
            print(f"  Copied: {file_name}")

        print()

        print("Step 2: Renaming directories and files...")

        current_year = datetime.datetime.now().year
        preserve_case = is_camel_case(project_name)

        replacements = {
            "baseproject": new_package_name,
            "BaseProject": project_name.replace(project_name[0], project_name[0].upper()) if preserve_case else new_package_name,
            "0.0.0": "0.0.1",
            "BASEP": f"{project_name}",
            "from baseproject.base": f"from {new_package_name}.base",
            "baseproject.baseproject": f"{new_package_name}.{new_package_name}",
            'PROG_COMPANY = "Company Name"': f'PROG_COMPANY = "{program_company}"',
            'Original author: ...': f'Original author: {author_name} <{author_email}>',
            'Python Base Project': f'{program_name}',
        }

        # Step 2.1: Find and rename the entry file first (before directory rename)
        old_package_dir = new_src_dir / "baseproject"
        new_package_name_dir = new_src_dir / new_package_name

        if not old_package_dir.is_dir():
            print(f"ERROR: Package directory not found: {old_package_dir}", file=sys.stderr)
            print(f"This may indicate a template structure change.", file=sys.stderr)
            sys.exit(1)

        # Check where the baseproject.py file is located
        possible_old_entry_files = [
            new_src_dir / "baseproject.py",
            old_package_dir / "baseproject.py",
        ]
        old_entry_file = None
        for candidate in possible_old_entry_files:
            if candidate.is_file():
                old_entry_file = candidate
                break

        if not old_entry_file:
            print(f"ERROR: Entry file not found in either location:", file=sys.stderr)
            print(f"  - {new_src_dir / 'baseproject.py'}", file=sys.stderr)
            print(f"  - {old_package_dir / 'baseproject.py'}", file=sys.stderr)
            sys.exit(1)

        # Rename the file to match package name
        new_entry_name = new_package_name + ".py"
        new_entry_file = old_entry_file.parent / new_entry_name
        old_entry_file.rename(str(new_entry_file))
        print(f"  Renamed: baseproject.py => {new_entry_name} ({new_entry_file.parent})")

        # Step 2.2: Rename the directory
        if new_package_name_dir.exists():
            print(f"Destination '{new_package_name_dir}' exists, removing...")
            shutil.rmtree(new_package_name_dir)
        old_package_dir.rename(str(new_package_name_dir))
        print(f"  Renamed: {old_package_dir} => {new_package_name_dir}")
        print()

        # Step 3: Process pyproject.toml
        print("Step 3: Processing pyproject.toml...")
        pyproject_toml_path = new_project_path / "pyproject.toml"
        if pyproject_toml_path.exists():
            process_toml_file(
                pyproject_toml_path,
                new_package_name,
                project_name,
                author_name,
                author_email,
                str(current_year)
            )

        # Step 4: Apply text replacements to Python files
        print("Step 4: Applying text replacements to Python files...")

        for file_path in new_project_path.rglob("*"):
            if file_path.is_file() and file_path.suffix == ".py":
                process_file(
                    file_path,
                    replacements,
                    str(current_year),
                    author_name,
                    author_email
                )

        print("Text replacements completed.")

        if preserve_case:
            print(f"Note: CamelCase detected, preserving {project_name} format")

        print()
        print("="*60)
        print("SUCCESS! New project created at:")
        print(f"  {new_project_path}")
        print()
        print("Next steps:")
        print(f"  cd {new_project_path.name}")
        print("  poetry install")
        print("  poetry run pytest")
        print("="*60 + "\n")

    except FileNotFoundError as e:
        print(f"\n\u2717 Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\u2717 Operation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\u2717 Unexpected error during project bootstrap: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

    finally:
        os.chdir(original_dir)


def print_help() -> None:
    """Print script usage information."""
    script_name = os.path.basename(sys.argv[0])
    print(f"""Usage:
  {script_name} [OPTIONS] PROJECT_NAME PROJECT_LOCATION
  {script_name} [OPTIONS]

Bootstrap a new Python CLI project

Positional Arguments:
  PROJECT_NAME       The name of the new project (e.g., my-awesome-tool)
  PROJECT_LOCATION   The directory path to create the project

Options:
  -h, --help         Show this help message and exit
  -a, --auto         Non-interactive mode (assumes yes to prompts)
  -i, --interactive  Force interactive mode
  --help-command     Show additional command-line help

Examples:
  # Interactive mode (default)
  {script_name}

  # With project name and location
  {script_name} my-tool ~/projects

  # Auto mode (non-interactive)
  {script_name} --auto my-tool ~/projects
""")


def parse_arguments():
    """Parse command line arguments.

    Returns:
        Namespace object containing parsed arguments
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Bootstrap a new Python CLI project from template",
        epilog="""Examples:
  %(prog)s                              Run in interactive mode
  %(prog)s my-tool ~/projects           Create project at specific location
  %(prog)s --auto my-tool ~/projects    Non-interactive, auto-accept prompts
"""
    )

    parser.add_argument(
        "-a", "--auto",
        action="store_true",
        help="Disable interactive prompts, assume 'yes' to all"
    )

    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Force interactive prompting mode"
    )

    parser.add_argument(
        "--help-command",
        action="store_true",
        help="Show additional command-line help"
    )

    parser.add_argument(
        "project_name",
        nargs="?",
        type=str,
        help="Name of the new project"
    )

    parser.add_argument(
        "project_location",
        nargs="?",
        type=str,
        help="Directory path to create the new project"
    )

    args = parser.parse_args()

    if args.help_command:
        print_help()
        sys.exit(0)

    return args


def main(interactive: bool = True, auto: bool = False) -> None:
    """Main entry point for the script.

    Args:
        interactive: Run in interactive mode
        auto: Run in automated non-interactive mode
    """
    args = parse_arguments()

    use_auto = auto or args.auto
    use_interactive = interactive or args.interactive

    # Step 1: Get the project name
    project_name = args.project_name

    if not project_name:
        if use_auto:
            project_name = "my-project"
        elif use_interactive:
            print(f"\n--- Project name ---")
            project_name = prompt_project_name()
        else:
            print("Error: Project name is required.")
            sys.exit(1)

    # Step 2: Get the project location
    project_location = args.project_location

    if not project_location:
        if use_auto:
            project_location = "./my-project"
        elif use_interactive:
            print(f"\n--- Project location ---")
            project_location = prompt_project_location()
        else:
            print("Error: Project location is required.")
            sys.exit(1)

    # Step 3: Get user information
    if use_auto:
        author_name = "Auto Generated User"
        author_email = "auto@example.com"
        program_name = "My Custom Program"
        program_company = "Company Name"
        print(f"\n[Auto: Using generic project info]")
        print(f"Author: {author_name} <{author_email}>")
        print(f"Program: {program_name}")
        print(f"Company: {program_company}\n")
    else:
        print("\n--- Project Information ---")
        author_name, author_email, program_name, program_company = get_user_info()

    # Step 4: Bootstrap the project
    keep = use_auto
    bootstrap_project(
        project_name=project_name,
        location=project_location,
        author_name=author_name,
        author_email=author_email,
        program_name=program_name,
        program_company=program_company,
        keep_template=keep
    )


if __name__ == "__main__":
    main()
