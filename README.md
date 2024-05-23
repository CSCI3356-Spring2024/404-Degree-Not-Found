# EaglePlan
## Overview
EaglePlan is a web-based academic planning tool designed specifically for Boston College students. The software was developed to streamline the course planning process, making it easy and reliable for students to organize their academic careers effectively. This tool supports students in searching for courses, adding them to their semester plans, and ensuring these plans align with graduation and major/minor requirements. The flexibility of EaglePlan allows for real-time adjustments and verifications, providing a user-friendly interface to facilitate academic planning.

## Motivation
The development of EaglePlan was motivated by the need for a centralized, intuitive planning tool that alleviates the common challenges faced by students when mapping out their academic journeys. By integrating directly with Boston College systems through the EagleApps API, EaglePlan ensures that students have access to up-to-date course information and requirements, empowering them to make informed decisions about their educational paths.

## Features
* Dynamic Course Search and Planning: Allows students to search for courses and add them to their 4-year plan.
* Real-Time Validation: Automatically verifies if the planned courses meet the requirements for graduation and major/minor specifications.
* Google OAuth Integration: Ensures secure and straightforward access using Boston College credentials.
* Admin and Advisor Access: Provides aggregate data to help departments plan course offerings based on student interest.

## Technologies Used
Frontend: HTML, CSS, Bootstrap
Backend: Django
Authentication: Google OAuth
API Integration: EagleApps API for fetching course and requirement data

## Login Page
<img width="1660" alt="Login Page" src="https://github.com/CSCI3356-Spring2024/404-Degree-Not-Found/assets/89826556/9a63cf4b-665f-4047-b856-4289d212d46a">
<img width="1659" alt="Google Login" src="https://github.com/CSCI3356-Spring2024/404-Degree-Not-Found/assets/89826556/07bf6efd-835f-449b-996c-a71e79a8727e">

The login page utilizes Google OAuth for authentication, ensuring that all users are verified Boston College students or staff.

## Landing Page
<img width="1659" alt="Landing Page" src="https://github.com/CSCI3356-Spring2024/404-Degree-Not-Found/assets/89826556/8782a778-e8f9-4ca1-b7d6-858490a53820">

The landing page provides an overview of a student’s progress towards their Major(s) Requirements, University Core Requirements, and Total Credits. Visual progress bars show completion percentages, helping students easily track their academic progress and identify areas that need attention.

## Profile Page
<img width="1660" alt="User Profile" src="https://github.com/CSCI3356-Spring2024/404-Degree-Not-Found/assets/89826556/886945de-1b9a-4efe-9499-2f1f7a4c3163">

The profile page allows students to enter and edit their educational details such as school, major(s), minor(s), entry year and semester, and expected graduation year. This page facilitates the customization and accuracy of their academic plan.


## Four-Year Plan Overview
<img width="1663" alt="4 Year Plan" src="https://github.com/CSCI3356-Spring2024/404-Degree-Not-Found/assets/89826556/1e488a83-51fd-4c7d-bac9-d5eeb858c332">

The 4-year plan page allows students to visualize their entire academic plan, adjust semesters, and check completion progress.

## Course Search and Plan Management
<img width="1661" alt="Add Course" src="https://github.com/CSCI3356-Spring2024/404-Degree-Not-Found/assets/89826556/a375ff96-f77b-4f80-a1c2-5929de8c8fda">

Students can search for courses, view details, and add them to their academic plans.

## Requirement Verification
<img width="1660" alt="Requirements Verification" src="https://github.com/CSCI3356-Spring2024/404-Degree-Not-Found/assets/89826556/7c46b552-b0a3-4a36-adcd-bc7de0893188">

EaglePlan automatically verifies that each student’s course selections meet their major and graduation requirements. It also verifies whether prerequisite requirements have been met.

## Limitations and Deployment
Due to restrictions in deploying the EagleApps API, EaglePlan is currently not hosted online. The API is restricted for internal use within Boston College's network to ensure data security and integrity.
