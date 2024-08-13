## GRADUATION THESIS - IMPROVE THE TESTCASE RECOMMENDATION SYSTEM BY INCORPORATING TIME FACTORS
- **Instructors**:
    - Ths. Vu Van Tien
    - Ths. Tran Huy
- **Authors**: 
    - Nguyen Doan Nhat Minh
    - Vu Dang Khoa
- pdf file: Bao-CaoDATN.pdf - not final file

**Source code: https://github.com/ndnhatminh/sys**
### INTRODUCTION
- **The Testcase Recommendation System (TRS)** is the Recommendation System that aims to suggest suitable testcases for students based on their performances (the ability to solve assignment in Foundation Programming, Data Structure & Algorithm).
  - **Example**: System has 1000 testcases (#1, #2...,#100), student A has only passed 500/1000 testcases. The system would only provide a small testcase set that they had failed, like: #3, #4, #5 (that the Recommendation predict they would be most likely to solve that problem successfully the next time).
- The soul model of the **TRS**, RSVD model, was used to predict the student's correct answer for each testcase. Then some testcase that have mostly ability to solve would be choose to suggest to students. 
- **This thesis** enhances the TRS by researching the time factors and apply them by using AI model that incorporate time factors like: timeSVD, LSTM. Also, We build a custom web application to deploy them to students. The deployment had been successfull in 2 courses in the Computer Science field in Bach Khoa University.
### 🎯Features Built
#### Lecturers

1. Log in to the system using Google email.
2. Create, view, and edit created assignments (or assignments added by other lecturers).
3. Register multiple students for an assignment by uploading a CSV file with the list of students (file must follow the correct format from the BKEL system).
4. Add lecturers to the assignment.
5. View the list of students for the assignment.
#### Students

1. Log in to the system using the school-provided Google email.
2. View assignments they have been registered for.
3. Create new submissions.
4. View the status and suggested test cases of their submissions.
5. Fill out surveys.

### KEY POINTS

- **SYSTEM OVERVIEW**
![System Overview](general-system.png)

- **RELATIONAL DATABASE DIAGRAM**
![Relational database diagram](relational-database-diagram.png)

- **PROJECT STRUCTURES**
```
Grader
|
```
- ## 🦫 Results
1. UI
![rcm_ui_1](https://github.com/user-attachments/assets/f5c9c0dd-1a59-414f-a190-7623d6a1df8c)
![rcm_ui_2](https://github.com/user-attachments/assets/e1996a67-54e5-4019-af43-2c97b22005aa)
![rcm_ui_3](https://github.com/user-attachments/assets/edf27d91-43cd-4036-b658-08ddc46e861f)

## CONFERENCE PAPER - AN EVALUATION OF TESTCASE RECOMMENDATION SYSTEMS THROUGH FEEDBACK MODEL
- Authors: Many authors (for more detail please open this pdf file).
- pdf file: ICICCT-085_TRSReedback_Final.pdf - final file

- certificate: 51-2.pdf
