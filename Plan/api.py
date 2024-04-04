import requests

def fetch_course_data(course_code):
    base_url = 'http://localhost:8080/planning/planningcourses'
    params = {'code': course_code}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if data and isinstance(data, list) and len(data) > 0:            
            course = data[0].get('course', {})
            return {
                'name': course.get('name', 'No name available'),
                'description': course.get('descr', {}).get('plain', 'No description available'),
                'course_code': course.get('courseCode', 'No course code available'),
                'title': course.get('title', 'No title available')
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
                    courses.append({
                        'name': course.get('name', 'No name available'),
                        'description': course.get('descr', {}).get('plain', 'No description available'),
                        'course_code': course.get('courseCode', 'No course code available'),
                        'title': course.get('title', 'No title available')
                    })
        return courses
    except requests.exceptions.RequestException as e:
        print(e)
        return []