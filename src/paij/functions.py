import os
import shutil
import subprocess
import openai
import requests
import config


def generate_method_from_tests(api_key, unit_tests, language="Java"):
    openai.api_key = api_key
    prompt = f"""
           Write the corresponding {language} method that satisfies the following unit tests:
           {unit_tests}

           Note:
           - Do not include any imports related to testing frameworks such as JUnit or Mockito.
           - Only include necessary imports for the functionality of the generated methods.
           - Do not provide explanations, just the complete class and package name.
           - Make the class name {config.CLASS_NAME}

           Method:
           """
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": "You are a helpful assistant that writes up to multiple methods to satisfy unit tests. "
                        "Please complete all methods and write the best possible code"
             },
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,  # Adjust the length based on your need
        temperature=0.5
    )

    method_code = response.choices[0].message['content'].strip()
    method_code = method_code.replace('```java', '').replace('```', '').rstrip()

    return method_code


class PAiJ:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key

    @staticmethod
    def read_from_file(filename):
        with open(filename, 'r') as file:
            content = file.read()
        return content

    @staticmethod
    def write_to_file(filename, content):
        with open(filename, 'w') as file:
            file.write(content)

    @staticmethod
    def download_file(url, dest):
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(dest, 'wb') as file:
                shutil.copyfileobj(response.raw, file)

    @staticmethod
    def create_project_structure(base_dir, project_name):
        project_path = os.path.join(base_dir, project_name)
        os.makedirs(project_path, exist_ok=True)
        return project_path

    @staticmethod
    def run_maven_commands(maven_home, project_dir, test_class_name, max_retries=3):
        maven_executable = os.path.join(maven_home, 'mvn')
        retries = 0

        while retries < max_retries:
            compile_process = subprocess.run(
                [maven_executable, "clean", "compile", "test-compile"],
                cwd=project_dir,
                capture_output=True, text=True, shell=True
            )

            if compile_process.returncode != 0:
                print(f"Compilation failed:\n{compile_process.stderr}")
                return False
            else:
                print("Compilation successful.")

                test_process = subprocess.run(
                    [maven_executable, "test", f"-Dtest={test_class_name}"],
                    cwd=project_dir,
                    capture_output=True, text=True, shell=True
                )

                if test_process.returncode != 0:
                    print(f"Test execution failed (attempt {retries + 1}/{max_retries}):\n{test_process.stderr}")
                    retries += 1

                    if retries < max_retries:
                        print("Regenerating method from tests and retrying...")

                        unit_tests = PAiJ.read_from_file(config.INPUT_FILENAME)
                        method_code = generate_method_from_tests(unit_tests, language="Java")

                        # Write regenerated method to file
                        base_dir = os.path.join(config.SRC_PATH, 'main', 'java', *config.WHOLE_PACKAGE_NAME.split('.'))
                        project_name = config.PACKAGE_NAME
                        project_path = PAiJ.create_project_structure(base_dir, project_name)

                        method_code_lines = method_code.split('\n')
                        cleaned_method_code_lines = [line for line in method_code_lines if
                                                     not line.startswith('package')]
                        cleaned_method_code = '\n'.join(cleaned_method_code_lines)

                        class_code = f"""
                            package {config.WHOLE_PACKAGE_NAME}.{project_name};

                            {cleaned_method_code}
                            """

                        PAiJ.write_to_file(
                            os.path.join(project_path, f"{config.CLASS_NAME}.java"),
                            class_code)
                else:
                    print("Test execution successful.")
                    print(test_process.stdout)
                    return True

        print("Test execution failed after maximum retries.")
        return False
