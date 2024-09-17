import os 
import requests
import markdown 

from dotenv import load_dotenv

load_dotenv()
CANVAS_API_KEY= os.environ["CANVAS_API_KEY"]


def markdown_to_html(markdown_text):
    # TODO: add the constant disability, mental and other stuff here. 
    return markdown.markdown(markdown_text)

def get_courses(api_url,access_token):

    endpoint = f"{api_url}/courses"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Make the GET request to retrieve the courses
    response = requests.get(endpoint, headers=headers)
    courses = response.json()

    course_info ={}
    for course in courses:
        course_id = course['id']
        course_name = course['name']
        course_info[course_name] =course_id
    return course_info


def post_to_canvas(course_id, syllabus_content, api_key, api_url="https://auburn.instructure.com/api/v1"):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # First, get the current syllabus content
    get_url = f"{api_url}/courses/{course_id}"
    try:
        response = requests.get(get_url, headers=headers)
        response.raise_for_status()
        current_syllabus = response.json().get('syllabus_body', '')
    except requests.RequestException as e:
        raise Exception(f"Failed to fetch current syllabus: {e}")

    # If there's existing content, clear it
    if current_syllabus:
        clear_data = {
            "course": {
                "syllabus_body": ""
            }
        }
        try:
            response = requests.put(get_url, headers=headers, json=clear_data)
            response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Failed to clear existing syllabus: {e}")

    # Now post the new syllabus content
    html_content = markdown_to_html(syllabus_content)
    data = {
        "course": {
            "syllabus_body": html_content
        }
    }

    try:
        response = requests.put(get_url, headers=headers, json=data)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        raise Exception(f"Failed to post new syllabus: {e}")
    

    
