import requests

def extract_credits(credit_option_id):
    prefix = "kuali.result.values.group.credit.degree."
    if credit_option_id.startswith(prefix):
        # Remove the prefix from the string
        credits_str = credit_option_id[len(prefix):]
        # Convert the remaining part to an integer
        credits = int(float(credits_str))
        return credits
    else:
        # If the prefix is not found, return 0 or handle the error as needed
        return 0  # or raise an exception, return None, etc.

def extract_prerequisites(course_data):
    prereq_data = course_data.get("prereqTerseTranslations", [])
    prerequisites = [prereq['translation']['plain'] for prereq in prereq_data]
    return prerequisites


def fetch_course_data(course_code):
    base_url = 'http://localhost:8080/planning/planningcourses'
    params = {'code': course_code}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if data and isinstance(data, list) and len(data) > 0:
            course = data[0].get('course', {})
            credit_option_ids = course.get('creditOptionIds', [])
            credits = extract_credits(credit_option_ids[0]) if credit_option_ids else 0
            prerequisites = extract_prerequisites(data[0])  # Ensure we pass the correct part of data
            return {
                'description': course.get('descr', {}).get('plain', 'No description available'),
                'course_code': course.get('courseCode', 'No course code available'),
                'title': course.get('title', 'No title available'),
                'credits': credits,
                'prerequisites': prerequisites
            }
        return None
    except requests.exceptions.RequestException as e:
        print(e)
        return None

    
def fetch_courses(course_term):
    base_url = 'http://localhost:8080/planning/planningcourses'
    params = {'code': course_term}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        courses = []
        if data and isinstance(data, list):
            for item in data:
                course = item.get('course', {})
                if course_term.lower() in course.get('courseCode', '').lower():
                    credit_option_ids = course.get('creditOptionIds', [])
                    if credit_option_ids:
                        credits = extract_credits(credit_option_ids[0])
                    else:
                        credits = 0  # Default value if no credits are found
                    course_info = {
                        'description': course.get('descr', {}).get('plain', 'No description available'),
                        'course_code': course.get('courseCode', 'No course code available'),
                        'title': course.get('title', 'No title available'),
                        'credits': credits
                    }
                    courses.append(course_info)
        return courses
    except requests.exceptions.RequestException as e:
        print(e)
        return []