import openai

import config


def get_feedback_for_method(api_key, method_code):
    openai.api_key = api_key
    prompt = f"Provide feedback and potential improvements for the following Java method:\n\n{method_code}\n\nFeedback:"

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": "You are a knowledgeable assistant that reviews and provides feedback on Java methods. Please suggest improvements or optimizations."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.5,
        api_key=config.OPENAI_API_KEY
    )

    feedback = response.choices[0].message['content'].strip()
    return feedback


def apply_feedback(api_key, method_code, feedback):
    openai.api_key = api_key
    prompt = (
        f"""Here is the feedback to improve the following Java method:\n\nMethod:\n{method_code}\n\n
        Feedback:\n{feedback}\n\nPlease update the method according to the feedback."
        
             Note:
               - Do not include any imports related to testing frameworks such as JUnit or Mockito.
               - Only include necessary imports for the functionality of the generated methods.
               - Do not provide explanations, just the complete class and package name.
               - Make the class name {config.CLASS_NAME}
               - Make sure of the implementation of all provided improvments
               
              """)
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": "You are a helpful assistant that can update code according to the given feedback."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.5,
        api_key=config.OPENAI_API_KEY
    )

    updated_method_code = response.choices[0].message['content'].strip()
    return updated_method_code


def save_feedback(feedback, feedback_file):
    with open(feedback_file, 'w') as file:
        file.write(feedback)
