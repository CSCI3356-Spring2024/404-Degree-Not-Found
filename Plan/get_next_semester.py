from datetime import datetime

def get_current_semester(entry_year):
    current_year = datetime.now().year
    current_month = datetime.now().month
    entry_year = int(entry_year)

    # Calculate the number of years since entry
    years_since_entry = current_year - entry_year

    # Calculate the total number of semesters (max 8)
    total_semesters = min(years_since_entry * 2, 8)

    # Calculate the current semester
    if current_month >= 8:  # If current month is August or later, consider it as Fall semester
        current_semester = years_since_entry * 2
    else:
        current_semester = years_since_entry * 2 - 1  # Otherwise, it's Spring semester

    print(current_semester)
    return current_semester, total_semesters

def get_upcoming_semesters(current_semester, total_semesters):
    current_year = datetime.now().year
    semester_count = 0

    semesters = {}

    while semester_count < total_semesters:
        if current_semester % 2 == 0:
            semester_name = f"Spring {current_year + (current_semester - 1) // 2}"
        else:
            semester_name = f"Fall {current_year + (current_semester - 1) // 2}"

        semester_num = f"s{current_semester}"
        semesters[semester_num] = semester_name
        current_semester += 1
        semester_count += 1

        # Reset current semester and increment year if it exceeds 8
        if current_semester > 8:
            current_semester = 1
            current_year += 1
        
        if semester_count > total_semesters:
            break
    print(semesters)
    return semesters

def get_total_semesters(entry_year):
    current_year = datetime.now().year
    entry_year = int(entry_year)  # Convert entry year to an integer
    years_since_entry = current_year - entry_year
    total_semesters = min(years_since_entry * 2, 8)  # Assuming a maximum of 8 semesters
    remaining_semesters = 8 - total_semesters
    print(remaining_semesters)
    return remaining_semesters

