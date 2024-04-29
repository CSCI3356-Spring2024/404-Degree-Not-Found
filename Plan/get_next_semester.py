from datetime import datetime

def get_current_semester(entry_year):
    current_year = datetime.now().year
    entry_year = int(entry_year)

    # Calculate the number of years since entry
    years_since_entry = current_year - entry_year

    # Calculate the total number of semesters (max 8)
    total_semesters = min(years_since_entry * 2, 8)
    print(total_semesters)

    # Calculate the current semester based on total semesters
    current_semester = total_semesters

    return current_semester, 8  # Return 8 as the total semesters since it's a fixed value for this application

def get_upcoming_semesters(current_semester):
    current_year = datetime.now().year

    semesters = {}
    year = current_year
    semester_count = 0

    while semester_count < 3:  # Get courses for the next 3 semesters
        if current_semester == 8:
            current_semester = 1
            year += 1

        semester_name = f"Spring {year}" if current_semester % 2 == 0 else f"Fall {year}"
        semester_num = f"s{current_semester}"
        semesters[semester_num] = semester_name

        current_semester += 1
        semester_count += 1

    return semesters
    
def get_course_semester(entry_year, semester_num):
    current_date = datetime.now()
    
    # Check if the student entry year is available
    if entry_year:
        entry_year = int(entry_year)
    else:
        # Handle the case where entry year is not available
        return "Unknown"

    # Determine the entry semester based on the student's entry year
    entry_semester = "Spring" if current_date.month < 8 else "Fall"

    # Calculate the difference in years between the current year and the entry year
    year_difference = current_date.year - entry_year

    # Calculate the current semester number based on the entry semester and the year difference
    current_semester_num = (year_difference * 2) + (1 if entry_semester == "Fall" else 0)

    # Extract the semester number from the semester_num variable
    semester_number = int(semester_num[1:])
    
    # Calculate the semester for the given semester number
    course_semester_num = current_semester_num + semester_number - 1
    course_semester_year = entry_year + (course_semester_num - 1) // 2
    course_semester = "Spring" if course_semester_num % 2 == 1 else "Fall"

    return f"{course_semester} {course_semester_year}"