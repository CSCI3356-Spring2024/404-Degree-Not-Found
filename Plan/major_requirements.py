def validate_major_requirements(plan, major):
    # Initialize major_requirements with a default value
    major_requirements = {}

    # Get the major requirements based on the student's major
    if major == "Computer Science BA":
        major_requirements = {
            "CSCI1101": 1,
            "CSCI1102": 1,
            "CSCI2243": 1,
            "CSCI2244": 1,
            "CSCI2271": 1,
            "CSCI2272": 1,
            "CSCI3383": 1,
            "CSCI2000+": (1, ["CSCI2243", "CSCI2244", "CSCI2271", "CSCI2272"]),
            "CSCI3000+": (3, ["CSCI3383"]),
        }
    elif major == "Computer Science BS":
        major_requirements = {
            "CSCI1101": 1,
            "CSCI1102": 1,
            "CSCI2243": 1,
            "CSCI2244": 1,
            "CSCI2271": 1,
            "CSCI2272": 1,
            "CSCI3383": 1,
            "CSCI2260-2267": (1, ["CSCI2260", "CSCI2261", "CSCI2262", "CSCI2263", "CSCI2264", "CSCI2265", "CSCI2266", "CSCI2267"]),
            "CSCI3000+": (4, ["CSCI3383"]),
            "MATH1103 or MATH1105": (1, ["MATH1103", "MATH1105"]),
            "MATH2202": 1,
            "MATH2210": 1,
            "MATH3000+": (1, ["MATH4426"]),
            "Science with Lab": (1, [
                # Biology options
                ["BIOL2000", "BIOL2010", "BIOL2040"],  # Option 1
                ["BIOL2000", "BIOL3030", "BIOL2040"],  # Option 2
                # Chemistry options
                ["CHEM1109", "CHEM1110"],  # Option 1
                ["CHEM1117", "CHEM1118"],  # Option 2
                # Physics options
                ["PHYS2200", "PHYS2201"],  # Option 1
                # Earth and Environmental Sciences options
                ["EESC1132", "EESC2202", "EESC2203"],  # Option 1
                ["EESC1132"],  # Option 2
                ["EESC2202", "EESC2203"],  # Option 3
            ]),
        }

    saved_courses = []
    for semester_num in ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8']:
        saved_courses.extend(plan.__dict__[semester_num])
        
    print(saved_courses)
    print("Major requirements:", major_requirements)

    requirements_met = {req: 0 for req in major_requirements}

    # Increment requirements met for each course in saved_courses
    for course in saved_courses:
        if course in major_requirements:
            requirements_met[course] += 1

    # Validate requirements
    for req, value in major_requirements.items():
        if req == "CSCI2000+":
            count_required, excluding_courses = value
            count_met = requirements_met[req]
            count_at_2000 = sum(1 for course in saved_courses if course.startswith("CSCI2") and course not in excluding_courses)
            print("Count at 2000 level:", count_at_2000)
            if count_at_2000 < count_required:
                print("Not enough courses at 2000 level.")
                return False
            for exc_course in excluding_courses:
                if exc_course in requirements_met:
                    # Subtract the count of exclusion courses from the total required count
                    count_required -= requirements_met[exc_course]
            if count_met < count_required:
                print("Not enough valid courses at 2000 level.")
                return False
        elif req == "CSCI3000+":
            count_required, excluding_courses = value
            count_met = requirements_met[req]
            count_above_3000 = sum(1 for course in saved_courses if course.startswith("CSCI3") and course not in excluding_courses)
            print("Count above 3000 level:", count_above_3000)
            for course in saved_courses:
                if course.startswith("CSCI3") and course not in excluding_courses:
                    print("Evaluating course:", course)
                    # Update count_met when a valid 3000 level course is encountered
                    count_met += 1
            if count_above_3000 < count_required:
                print("Not enough courses above 3000 level.")
                return False
            for exc_course in excluding_courses:
                if exc_course in requirements_met:
                    # Subtract the count of exclusion courses from the total required count
                    count_required -= requirements_met[exc_course]
            if count_met < count_required:
                print("Not enough valid courses above 3000 level.")
                return False
        elif req == "MATH1103 or MATH1105":
            count_required, courses = value
            count_met = requirements_met[req]
            for course in courses:
                if course in saved_courses:
                    count_met += 1
            if count_met < count_required:
                print("Not enough valid courses for MATH1103 or MATH1105.")
                return False
        elif req == "MATH3000+":
            count_required, excluding_courses = value
            count_met = requirements_met[req]
            count_math_3000 = sum(1 for course in saved_courses if course.startswith("MATH") and course != "MATH4426" and course not in excluding_courses)
            print("Count at 3000 level:", count_math_3000)
            if count_math_3000 < count_required:
                print("Not enough valid courses at 3000 level.")
                return False
            for exc_course in excluding_courses:
                if exc_course in requirements_met:
                    # Subtract the count of exclusion courses from the total required count
                    count_required -= requirements_met[exc_course]
            if count_met < count_required:
                print("Not enough valid courses at 3000 level.")
                return False
        elif req == "Science with Lab":
            count_required, courses = value
            count_met = requirements_met[req]
            for option in courses:
                if all(course in saved_courses for course in option):
                    count_met += 1
                    break  # Stop loop once one option is satisfied
            if count_met < count_required:
                print("Not enough valid science courses with lab.")
                return False
        elif isinstance(value, tuple):
            count_required, _ = value
            if requirements_met[req] < count_required:
                return False
    
    return True