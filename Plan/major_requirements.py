


def validate_major_requirements(plan, major, saved_courses = None):
    # Initialize major_requirements with a default value
    major_requirements = {}

    if saved_courses == None:
        saved_courses = []
        for semester_num in ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8']:
            saved_courses.extend(plan.__dict__[semester_num])
        print("Entire Progress")
    else:
        print("Completed Progress")
        
    # A function that checks if a single course is in the plan
    def course_in_plan(course_code):
        if course_code in saved_courses:
            return 1, None
        else:
            return 0, f"{course_code} is not taken"
    
    # A function that checks if course A OR course B is in the plan
    def courseAorB_in_plan(courseA, courseB):
        if courseA in saved_courses or courseB in saved_courses:
            return 1, None
        else:
            return 0, f"{courseA} or {courseB} is not taken"
        
    # A function that checks the number of electives at a certain level in the plan
    # Excludes certain courses
    def countCoursesAtLevel(course_level, except_courses, required_number):
        count = 0
        for course in saved_courses:
            if (course.startswith(course_level)) and (course not in except_courses):
                count += 1

        if count >= required_number:
            return required_number, None
        else:
            return count, f"{count} {course_level}000 courses have been taken. Need {required_number-count} more."
    
    # A function that counts the number of courses completed for a series of courses.
    # The student has the option to select which series of course to take
    # Designed for the Science Component for CS BS req
    def countCompletedSeriesCourses(options, required_number):
        count = 0
        for option in options:
            optioncount = sum(1 for course in options if course in saved_courses)
            count = max(count, optioncount)
        if count >= required_number:
            return required_number, None
        else:
            return count, f"Science requirements for CS BS not met"

    # Get the major requirements based on the student's major
    if major == "Undeclared":
        return 0, 100, ["You have not declared a major yet"]
    elif major == "Computer Science BA":
        major_requirements = (11,[course_in_plan("CSCI1101"),
                                  course_in_plan("CSCI1102"),
                                  course_in_plan("CSCI2243"),
                                  course_in_plan("CSCI2244"),
                                  course_in_plan("CSCI2271"),
                                  course_in_plan("CSCI2272"),
                                  course_in_plan("CSCI3383"),
                                  countCoursesAtLevel("CSCI2",["CSCI2243", "CSCI2244", "CSCI2271", "CSCI2272"],1),
                                  countCoursesAtLevel("CSCI3",["CSCI3383"],3)]
                            )
    elif major == "Computer Science BS":
        major_requirements = (18,[course_in_plan("CSCI1101"),
                                  course_in_plan("CSCI1102"),
                                  course_in_plan("CSCI2243"),
                                  course_in_plan("CSCI2244"),
                                  course_in_plan("CSCI2271"),
                                  course_in_plan("CSCI2272"),
                                  course_in_plan("CSCI3383"),
                                  course_in_plan("CSCI2267"),
                                  countCoursesAtLevel("CSCI3",["CSCI3383"],4),
                                  courseAorB_in_plan("MATH1103", "MATH1105"),
                                  course_in_plan("CSCI2202"),
                                  course_in_plan("CSCI2210"),
                                  countCoursesAtLevel("MATH3",["MATH4426"],1),
                                  countCompletedSeriesCourses([["BIOL2000", "BIOL2010"],["BIOL2000", "BIOL3030"],["CHEM1109", "CHEM1110"],["CHEM1117", "CHEM1118"],["PHYS2200", "PHYS2201"]],2)]   
                            )

    elif major == "Economics":
        major_requirements = (11,[course_in_plan("ECON1101"),
                                  course_in_plan("ECON1151"),
                                  course_in_plan("ECON2201"),
                                  course_in_plan("ECON2202"),
                                  course_in_plan("ECON2228"),
                                  countCoursesAtLevel("ECON2",["ECON2201, ECON2202, ECON2228"],2),
                                  countCoursesAtLevel("ECON3",[],4),
                                  course_in_plan("MATH1102")
                                  ]
                            )

    finished_req = 0
    errormessages = []
    print("MAJOR REQ")
    print(saved_courses)
    print(major)
    print(major_requirements)
    print()
    print()
    
    for req in major_requirements[1]:
        finished_req += req[0]
        if req[1]:
            errormessages.append(req[1])
    
    return finished_req, major_requirements[0], errormessages

           
         