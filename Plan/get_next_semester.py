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
    print(current_semester)
    return current_semester, 8  # Return 8 as the total semesters since it's a fixed value for this application

def get_upcoming_semesters(current_semester, total_semesters):
    current_year = datetime.now().year

    semesters = {}
    year = current_year
    semester_count = 0

    while semester_count < total_semesters + 1:
        if current_semester % 2 == 0:
            semester_name = f"Spring {year}" if current_semester != 8 else f"Spring {year + 1}"
        else:
            semester_name = f"Fall {year}"
        semester_num = f"s{current_semester}"
        semesters[semester_num] = semester_name

        if current_semester == 8:
            current_semester = 1
            year += 1
        else:
            current_semester += 1
        
        semester_count += 1

    return semesters

def get_total_semesters(entry_year):
    current_year = datetime.now().year
    entry_year = int(entry_year)  # Convert entry year to an integer
    years_since_entry = current_year - entry_year
    total_semesters = min(years_since_entry * 2, 8)  # Assuming a maximum of 8 semesters
    remaining_semesters = 8 - total_semesters
    print(remaining_semesters)
    return remaining_semesters