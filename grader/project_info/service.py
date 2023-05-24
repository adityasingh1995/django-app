import json
from pathlib import Path
import urllib.parse as urlparse
import requests


project_submission_types = {
    'fruit_search': 'git'
}


def get_project_info(project_name):
    project_dir = Path(__file__).parent / project_name

    if project_name == 'fruit_search':
        detail = json.dumps(json.load(open(f'{project_dir}/fruitsearchproject.json')))
        rubric = json.dumps(json.load(open(f'{project_dir}/rubrics.json')))

        def get_solution_files(solutions_path):
            starter_index_html = None
            with open(f'{solutions_path}/index.html') as file:
                starter_index_html = file.read()

            starter_script_js = None
            with open(f'{solutions_path}/script.js') as file:
                starter_script_js = file.read()

            starter_style_css = None
            with open(f'{solutions_path}/style.css') as file:
                starter_style_css = file.read()

            return starter_index_html, starter_script_js, starter_style_css

        # get good solution
        starter_index_html, starter_script_js, starter_style_css = get_solution_files(f'{project_dir}/starter_code')
        # good_index_html, good_script_js, good_style_css = get_solution_files(f'{project_dir}/good_solution')
        # bad_1_index_html, bad_1_script_js, bad_1_style_css = get_solution_files(f'{project_dir}/bad_solution_1')

        context_prompt = f"""
        You are a evaluator who evaluates project submission submitted by students of a software engineering course
        Here are the project details demarcated by triple backticks:
        
        ```
        {detail}
        ```
        
        Here is the rubric on which on the basic of which the submission must be evaluated, demarcated by triple backticks
        
        ```
        {rubric}
        ```
        
        Here is the starter code based on which the student has to write the complete solution
        
        Html file
        ```
        {starter_index_html}
        ```

        javascript file
        ```
        {starter_script_js}
        ```

        css file

        ```
        {starter_style_css}
        ```
        """

        # Following files are an example of correct solution
        #
        # Html file
        # ```
        # {good_index_html}
        # ```
        #
        # javascript file
        # ```
        # {good_script_js}
        # ```
        #
        # css file
        #
        # ```
        # {good_style_css}
        # ```
        #
        # Based on the above project details, evaluation criteria and code submitted by student, Share exact details of
        # where the code would or would not meet expectations as per the rubrics shared.
        # """

        return context_prompt

    if project_name == 'software_test':
        detail = json.dumps(json.load(open(f'{project_dir}/softwaretestproject.json')))
        questions = json.dumps(json.load(open(f'{project_dir}/questions.json')))
        context_prompt = f"""
        You are a evaluator who evaluates project submission submitted by students of a cyber security engineering course
        Here are the project details demarcated by triple backticks:

        ```
        {detail}
        ```
        
        Here are the questions a student is supposed to answer as part of their project submission.
        
        ```
        {questions}
        ```
        
        """
        return context_prompt


def get_solution_text(project_name, git_link):
    if 'github.com' not in git_link:
        return None

    if project_name == 'fruit_search':
        parsed_url = urlparse.urlparse(git_link)
        path = parsed_url.path

        raw_path = f'https://raw.githubusercontent.com{path}'
        raw_path = raw_path.strip('/')

        html_file_path = '/'.join([raw_path, 'main', 'index.html'])
        js_file_path = '/'.join([raw_path, 'main', 'script.js'])
        style_file_path = '/'.join([raw_path, 'main', 'style.css'])

        html_file_string = requests.get(html_file_path)
        html_file_string = html_file_string.text

        js_file_string = requests.get(js_file_path)
        js_file_string = js_file_string.text

        style_file_string = requests.get(style_file_path)
        style_file_string = style_file_string.text

        return f"""
            Solution submitted by student is as follows 
            
            html file demarcated by triple backticks:
            ```
            {html_file_string}
            ```
            
            js file demarcated by triple backticks:
            
            ```
            {js_file_string}
            ```
            
            
            css file demarcated by triple backticks
            
            ```
            {style_file_string}
            ```
        Based on the project rubrics, generate the correct code for this project using the starter code.
        Go through the completion conditions one by one and check if the solution provided by the student 
        meets the criteria by comparing with your generated solution.
        Share exact details of where the code would or would not meet expectations as per the rubrics shared.
        Share the parts of the student's code which do no match with your generated solution    
        """

    if project_name == 'software_test':
        parsed_url = urlparse.urlparse(git_link)
        path = parsed_url.path

        raw_path = f'https://raw.githubusercontent.com{path}'
        raw_path = raw_path.strip('/')

        answer_file_path = '/'.join([raw_path, 'main', 'answer.txt'])

        answer_file_string = requests.get(answer_file_path)
        answer_file_string = answer_file_string.text

        return f"""
           Solution submitted by student is as follows 

           answer file demarcated by triple backticks:
           ```
           {answer_file_string}
           ```
        Based on the project detail, evaluate the answers submitted by the student in the answer.txt file
        Share the parts of the student's answer do no match the expectation.
        Share feedback for student for each question on a scale of 1 to 10 where 10 denotes excellent knowledge and 1 
        denotes poor knowledge     
        """


