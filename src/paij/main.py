import os

from paij.functions import *
from config import *
from paij.functions import PAiJ

from src.paij.feedback import *


def main():
    base_dir = os.path.join(SRC_PATH, 'main', 'java', *WHOLE_PACKAGE_NAME.split('.'))
    # test_dir = os.path.join(SRC_PATH, 'test', 'java', *WHOLE_PACKAGE_NAME.split('.'))

    project_name = PACKAGE_NAME
    input_filename = INPUT_FILENAME

    unit_tests = PAiJ.read_from_file(input_filename)
    method_code = generate_method_from_tests(OPENAI_API_KEY, unit_tests, language="Java")

    project_path = PAiJ.create_project_structure(base_dir, project_name)

    method_code_lines = method_code.split('\n')
    cleaned_method_code_lines = [line for line in method_code_lines if not line.startswith('package')]
    cleaned_method_code = '\n'.join(cleaned_method_code_lines)

    class_code = f"""
        package {WHOLE_PACKAGE_NAME}.{project_name};

        {cleaned_method_code}
        """

    class_file_path = os.path.join(project_path, f"{CLASS_NAME}.java")
    PAiJ.write_to_file(class_file_path, class_code)
    print(f"Generated project structure with class files in {project_path}")

    feedback = get_feedback_for_method(OPENAI_API_KEY, class_code)
    feedback_file_path = os.path.join(project_path, "feedback.txt")
    save_feedback(feedback, feedback_file_path)
    print(f"Feedback saved to {feedback_file_path}")

    updated_method_code = apply_feedback(OPENAI_API_KEY, class_code, feedback)
    updated_method_code = updated_method_code.replace('```java', '').replace('```', '').rstrip()

    PAiJ.write_to_file(class_file_path, updated_method_code)
    print(f"Updated method code written to {class_file_path}")

    max_retries = 3
    retry_count = 0

    while retry_count < max_retries:
        if PAiJ.run_maven_commands(config.MAVEN_HOME, config.PROJECT_DIR, config.TEST_CLASS_NAME, max_retries):
            print("Maven build and tests were successful.")
            break
        else:
            retry_count += 1
            if retry_count >= max_retries:
                print("Maximum retries reached. Manual intervention required.")
                break

            print("Maven build or tests failed. Generating new method code...")

            method_code = generate_method_from_tests(config.OPENAI_API_KEY, unit_tests, language="Java")
            method_code_lines = method_code.split('\n')
            cleaned_method_code_lines = [line for line in method_code_lines if not line.startswith('package')]
            cleaned_method_code = '\n'.join(cleaned_method_code_lines)

            class_code = f"""
                   package {config.WHOLE_PACKAGE_NAME}.{project_name};

                   {cleaned_method_code}
                   """

            PAiJ.write_to_file(class_file_path, class_code)
            print(f"Generated new method code written to {class_file_path}")


if __name__ == "__main__":
    main()
