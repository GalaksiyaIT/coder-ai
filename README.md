# CoderAI

CoderAI is a Python library designed to generate Java methods from unit tests using OpenAI's GPT model. This tool is
currently designed specifically for Java and is still in the development process. Future versions may include support
for other languages.

## Features

- Generates Java methods that satisfy given unit tests.
- Reads unit tests from a file and processes them to generate corresponding Java methods.
- Creates a project structure for the generated code.
- Runs Maven commands to compile and test the generated Java code.

## Installation

```bash
pip install coder-ai
```

## Usage

### Example

Here's a basic example of how to use CoderAI:

1. Ensure you have your unit tests written in a file, for example, example_code.
2. Create a configuration file config.py with the necessary paths and API keys.

`config.py`

```
SRC_PATH = r'YOUR_SPRING_SRC_PATH'
PACKAGE_NAME = 'YOUR_PACKAGE_NAME_WILL_CREATED_INTO'
INPUT_FILENAME = 'YOUR_INPUT_FILENAME'
OPENAI_API_KEY = "YOUR_KEY"
MAVEN_HOME = r'YOUR_MAVEN/BIN_PATH'
PROJECT_DIR = r'YOUR_PROJECT_DIR'
WHOLE_PACKAGE_NAME = 'YOUR_MAIN_PACKAGE_NAME'
BASE_NAME = "YOUR_BASE_CLASS_NAME"
CLASS_NAME = 'YOUR_CLASS_NAME'
TEST_CLASS_NAME = 'YOUR_TEST_CLASS_NAME'
```

3. Use the main script to generate the methods and run Maven commands.

`main.py`

```
import os
import config
from coderai.functions import *
from coderai.functions import CoderAI

def main():
    base_dir = os.path.join(config.SRC_PATH, 'main', 'java', *config.PACKAGE_NAME.split('.'))
    test_dir = os.path.join(config.SRC_PATH, 'test', 'java', *config.PACKAGE_NAME.split('.'))

    project_name = config.PROJECT_NAME
    input_filename = config.INPUT_FILENAME

    unit_tests = read_from_file(input_filename)
    method_code = generate_method_from_tests(config.OPENAI_API_KEY, unit_tests, language="Java")

    project_path = create_project_structure(base_dir, project_name)
    test_path = create_project_structure(test_dir, project_name)

    import_package, real_codes = process_unit_tests(unit_tests)

    method_code_lines = method_code.split('\n')
    cleaned_method_code_lines = [line for line in method_code_lines if not line.startswith('package')]
    cleaned_method_code = '\n'.join(cleaned_method_code_lines)

    class_code = f"""
    package {config.PACKAGE_NAME}.{project_name};

    {import_package}

    {cleaned_method_code}
    """

    test_code = f"""
    package {config.PACKAGE_NAME}.{project_name};

    {unit_tests}
    """

    write_to_file(
        os.path.join(project_path, f"{config.CLASS_NAME}.java"),
        class_code)
    print(f"Generated project structure with class files in {project_path}")

    write_to_file(
        os.path.join(test_path, f"{config.TEST_CLASS_NAME}.java"),
        test_code)
    print(f"Generated project structure with test files in {test_path}")

    if run_maven_commands(config.MAVEN_HOME, config.PROJECT_DIR):
        print("Maven build and tests were successful.")
    else:
        print("Maven build or tests failed.")

if __name__ == "__main__":
    main()
```
### Functionality
- Reading Unit Tests: Reads unit tests from a specified file.
- Generating Methods: Uses OpenAI's GPT model to generate Java methods that satisfy the unit tests.
- Creating Project Structure: Creates the necessary directory structure for the Java project.
- Writing Code to Files: Writes the generated methods and unit tests to the appropriate Java files.
- Running Maven Commands: Compiles and tests the generated code using Maven.

## Development
- CoderAI is currently in the development phase. Contributions and feedback are welcome.

### Future Plans
- Add support for generating code in other programming languages.
- Improve the method generation logic and handle edge cases.
- Enhance the configuration options for more flexibility.

## License
This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.

## Contributing
1. Fork the repository
2. Create your feature branch (git checkout -b feature/AmazingFeature)
3. Commit your changes (git commit -m 'Add some AmazingFeature')
4. Push to the branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

