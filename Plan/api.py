import requests

def fetch_course_data(course_code):
    base_url = 'http://localhost:8080/planning/planningcourses'
    params = {'code': course_code}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        # Check if data is a list and has at least one item
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
