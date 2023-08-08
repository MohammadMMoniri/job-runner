import subprocess


def run_flake8_linter(code: str):
    # Write the code to a temporary file
    temp_file_path = "temp_code_file.py"
    with open(temp_file_path, "w") as temp_file:
        temp_file.write(code)

    # Run flake8 linter on the temporary file
    result = subprocess.run(["flake8", temp_file_path], capture_output=True, text=True)

    # Delete the temporary file
    subprocess.run(["rm", temp_file_path])

    # Get the linting errors, if any
    lint_errors = result.stdout.strip().split("\n") if result.returncode else []

    return lint_errors


def run_eslint(code: str):
    # Run eslint on the code
    result = subprocess.run(
        ["eslint", "--stdin"], input=code, capture_output=True, text=True
    )

    # Get the linting errors, if any
    lint_errors = result.stdout.strip().split("\n") if result.returncode else []

    return lint_errors


def run_checkstyle(code: str):
    # Write the code to a temporary file
    temp_file_path = "temp_code_file.java"
    with open(temp_file_path, "w") as temp_file:
        temp_file.write(code)

    # Run checkstyle on the temporary file
    result = subprocess.run(
        ["checkstyle", "-c", "checkstyle.xml", temp_file_path],
        capture_output=True,
        text=True,
    )

    # Delete the temporary file
    subprocess.run(["rm", temp_file_path])

    # Get the linting errors, if any
    lint_errors = result.stdout.strip().split("\n") if result.returncode else []

    return lint_errors
