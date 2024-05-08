
def validate_university_requirements(plan, saved_courses = []):
    # Initialize major_requirements with a default value

    if saved_courses == []:
        for semester_num in ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8']:
            saved_courses.extend(plan.__dict__[semester_num])
        
    # A function that returns the number of courses taken in the list of courses
    def countCoursesAtLevel(core, courselist, req):
        count = 0
        for course in courselist:
            if course in saved_courses:
                count += 1
        if count >= req:
            return max(count, req), None
        else:
            return count, f"{req-count} more {core} classes required"
    
    arts = ["AADS2250","ARTH1101","ARTH1102","ARTH1107","ARTH2212","ARTH2213","ARTH2231","ARTH2232","ARTH2250","ARTH2251","ARTH2257","ARTH2258","ARTH2274","ARTS1101","ARTS1102","ARTS1104","FILM1702","FILM2253","GERM2203","MUSA1100","MUSA1200"]
    diversity = ["AADS1104","AADS1110","AADS1114","AADS1137","AADS1137","AADS1139","AADS1155","AADS2199","AADS2250","AADS2306","AADS2470","AADS3310","AADS3340","APSY1031","ARTH2213","ARTH2250"]
    history1 = ["CLAS2206","HIST1001","HIST1077","HIST1091","HIST1113","HIST1816","HIST1822","HIST1841"]
    history2 = ["HIST1002","HIST1094","HIST1505","HIST1627","INTL2200","UNAS1716"]
    literature = ["CLAS1706","EALC2064","ENGL1080","ENGL1180","ENGL1184","ENGL1712","ENGL1721","ENGL1738","ENGL2210"]
    math = ["APSY2217","APSY2217","BZAN1135","CSCI1080","CSCI1101","MATH1004","MATH1007","MATH1100","MATH1101","MATH1102","MATH1103","MATH1190","MATH2202"]
    science = ["BIOL1100","BIOL1702","BIOL2000","BIOL2010","CHEM1105","CHEM1109","CHEM1117","EESC1132","EESC1150","EESC1170","EESC1180","EESC1704","ENGR1801","PHYS1100","PHYS1500","PHYS2100","PHYS2200","PSYC1110","UNAS1120"]
    phil = ["FORM1050","PHIL1070","PHIL1071","PHIL1088","PHIL1090","PHIL1109","PHIL1601","PHIL1603","PHIL1727","PHIL1729","PHIL2150","UNAS1105"]
    social = ["AADS1110","AADS1139","AADS1155","APSY1030","APSY1031","ECON1101","ECON1503","ECON1704","EDUC1030","EDUC1031","FORM1051","NURS1210","NURS2122","NURS4264","PHCG1210","POLI1021","POLI1041","POLI1042","POLI1061","POLI1091","PSYC1092","PSYC1111","SOCY1001","SOCY1002","SOCY1030","SOCY1036","SOCY1039","SOCY1043","SOCY1072","SOCY1089","SOCY1092","SOCY1500","SOCY1509","UNAS1110","UNAS1725","UNAS1733"]
    sacred_text = ["THEO1420","THEO1421","THEO1422","THEO1430","THEO1431","THEO1432","THEO1433","THEO1434"]
    christian_theology = ["THEO1401","THEO1402","THEO1701","THEO1729"]
    writing = ["ENGL1009","ENGL1010","ENGL1713"]

    university_requirements = (15,[countCoursesAtLevel("Arts",arts, 1),
                                   countCoursesAtLevel("Diversity",diversity, 1),
                                   countCoursesAtLevel("History 1",history1, 1),
                                   countCoursesAtLevel("History 2",history2, 1),
                                   countCoursesAtLevel("Literature",literature, 1),
                                   countCoursesAtLevel("Math",math, 1),
                                   countCoursesAtLevel("Science",science, 2),
                                   countCoursesAtLevel("Philosophy",phil, 2),
                                   countCoursesAtLevel("Social Science",social, 2),
                                   countCoursesAtLevel("Sacred Text",sacred_text, 1),
                                   countCoursesAtLevel("Christian Theology",christian_theology, 1),
                                   countCoursesAtLevel("Writing",writing, 1)
                                  ]
                            )

    finished_req = 0
    errormessages = []
    for req in university_requirements[1]:
        finished_req += req[0]
        if req[1]:
            errormessages.append(req[1])
    
    return finished_req, university_requirements[0], errormessages

           
         