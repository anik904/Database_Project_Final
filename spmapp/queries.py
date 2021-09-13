from django.db import connection
from spmapp.models import *
import numpy as np

studentlist = Student_T.objects.all()

programlist = Program_T.objects.all()

# Semesters Information


def getProgramWiseplo(program):
    with connection.cursor() as cursor:
        cursor.execute('''
             SELECT derived.plonum, avg(per)
             FROM(
                SELECT p.ploID as PLOID, p.ploNum as ploNum, 100*sum(e.obtainedMarks)/sum(a.TotalMarks) as per
                FROM spmapp_registration_t r,
                    spmapp_evaluation_t e,
                    spmapp_student_t st,
                    spmapp_program_t pr,
                    spmapp_assessment_t a,
                    spmapp_co_t c,
                    spmapp_plo_t p
                WHERE p.program_id = pr.programID
                    and e.reg_id = r.regID
                    and a.assessmentID = e.assessment_id
                    and a.coID_id = c.coID
                    and c.plo_id = p.ploID
                    and p.program_id = '{}'
                    GROUP BY p.ploID,r.student_id) derived
             GROUP BY derived.PLOID
                   '''.format(program))
        row = cursor.fetchall()
    plo = []
    avg = []
    for r in row:
        plo.append(r[0])
        avg.append(r[1])

    return plo, avg


def getPLO(course):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT p.ploNum

            FROM spmapp_course_t c,
                spmapp_co_t co,
                spmapp_plo_t p
            WHERE co.course_id = c.courseNum
                and co.plo_id = p.ploID
                and c.courseID = '{}'
        '''.format(course))

        row = cursor.fetchall()
    plo = []
    for r in row:
        plo.append(r[0])
    return plo


def getAllSemesters():
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT DISTINCT reg_semester || '2020'
            FROM spmapp_registration_t
        ''')

        row = cursor.fetchall()
    return row


def getCourseListOfAStudent(student):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT c.courseID
            FROM spmapp_course_t c,
                spmapp_section_t s,
                spmapp_registration_t r
            WHERE c.courseNum = s.course_id
                and s.sectionID = r.section_id
                and r.student_id = '{}'
        '''.format(student))
        row = cursor.fetchall()
    return row


def getProgramIDOfAUniversity(progName, uniID):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT p.programID
            FROM spmapp_program_t p,
                spmapp_department_t d,
                spmapp_school_t s,
                spmapp_university_t u
            WHERE p.department_id = d.departmentNum
                and d.school_id = s.schoolNum
                and s.university_id = u.universityID
                and p.programName = '{}'
                and u.universityID = '{}'
        '''.format(progName, uniID))
        row = cursor.fetchall()
    return row


def getDeptWisePLO(dept):
    with connection.cursor() as cursor:
        cursor.execute('''
             SELECT derived.plonum, avg(per)
             FROM(
                SELECT p.ploID as PLOID,p.ploNum as ploNum, 100*sum(e.obtainedMarks)/sum(a.TotalMarks) as per
                FROM spmapp_registration_t r,
                    spmapp_evaluation_t e,
                    spmapp_program_t pr,
                    spmapp_department_t d,
                    spmapp_assessment_t a,
                    spmapp_co_t c,
                    spmapp_plo_t p
                WHERE r.regID = e.reg_id
                    and pr.department_id = d.departmentNum
                    and a.assessmentID = e.assessment_id
                    and a.coID_id = c.coID
                    and c.plo_id = p.ploID
                    and p.program_id = pr.programID
                    and d.departmentNum = '{}'
                    GROUP BY p.ploNum,r.student_id) derived
             GROUP BY derived.ploNum
                   '''.format(dept))
        row = cursor.fetchall()
        row.sort(key=len)
    return row


# ******************************* Functionality : 1 *****************************
# 1a:  A chart showing percentage score in each PLO in a selected course against the average score (from the students in the same course).

def getStudentWiseePLO_course(studentID, course):
    with connection.cursor() as cursor:
        cursor.execute('''
                SELECT p.ploNum as plonum,100*(sum( e.obtainedMarks)/sum( a.totalMarks)) as plopercent
                FROM spmapp_registration_t r,
                    spmapp_assessment_t a,
                    spmapp_evaluation_t e,
                    spmapp_co_t co,
                    spmapp_plo_t p,
                    spmapp_course_t c
                WHERE  r.regID = e.reg_id
                    and e.assessment_id = a.assessmentID
                    and a.coID_id = co.coID
                    and co.plo_id = p.ploID
                    and co.course_id = c.courseNum
                    and  r.student_id = '{}'
                    and c.courseID = '{}'
                GROUP BY  p.ploID

                '''.format(studentID, course))
        row = cursor.fetchall()
    return row


def getCourseWisePLO(course, uni):
    with connection.cursor() as cursor:
        cursor.execute('''
             SELECT derived.plonum, avg(per)
             FROM(
                SELECT p.ploID as PLOID,p.ploNum as ploNum, 100*sum(e.obtainedMarks)/sum(a.TotalMarks) as per
                FROM spmapp_registration_t r,
                    spmapp_evaluation_t e,
                    spmapp_section_t s,
                    spmapp_course_t cr,
                    spmapp_program_t prog,
                    spmapp_department_t d,
                    spmapp_school_t sch,
                    spmapp_university_t u,
                    spmapp_assessment_t a,
                    spmapp_co_t c,
                    spmapp_plo_t p
                WHERE r.section_id = s.sectionID
                    and e.reg_id = r.regID
                    and a.assessmentID = e.assessment_id
                    and a.coID_id = c.coID
                    and c.plo_id = p.ploID
                    and c.course_id = cr.courseNum
                    and cr.program_id = prog.programID
                    and prog.department_id = d.departmentNum
                    and d.school_id = sch.schoolNum
                    and sch.university_id = u.universityID
                    and cr.courseID = '{}'
                    and u.universityID = '{}'
                    GROUP BY p.ploNum,r.student_id) derived
             GROUP BY derived.ploNum
                   '''.format(course, uni))
        row = cursor.fetchall()
        row.sort(key=len)
    return row


# 1b: A chart showing percentage score in each PLO against the program average (from the students in the same program).
def getStudentWisePLO_program(studentID):
    with connection.cursor() as cursor:
        cursor.execute('''
                SELECT p.ploNum as plonum,100*(sum( e.obtainedMarks)/sum( a.totalMarks)) as plopercent
                FROM spmapp_registration_t r,
                    spmapp_assessment_t a,
                    spmapp_evaluation_t e,
                    spmapp_co_t co,
                    spmapp_plo_t p
                WHERE  r.regID = e.reg_id
                    and e.assessment_id = a.assessmentID
                    and a.coID_id=co.coID
                    and co.plo_id = p.ploID
                    and  r.student_id = '{}'
                GROUP BY  p.ploID

                '''.format(studentID))
        row = cursor.fetchall()
    return row


def getProgramWisePLOpp(program):
    with connection.cursor() as cursor:
        cursor.execute('''
             SELECT derived.plonum, avg(per)
             FROM(
                SELECT p.ploID as PLOID, p.ploNum as ploNum, 100*sum(e.obtainedMarks)/sum(a.TotalMarks) as per
                FROM spmapp_registration_t r,
                    spmapp_evaluation_t e,
                    spmapp_program_t pr,
                    spmapp_assessment_t a,
                    spmapp_co_t c,
                    spmapp_plo_t p
                WHERE e.reg_id = r.regID
                    and a.assessmentID = e.assessment_id
                    and a.coID_id = c.coID
                    and c.plo_id = p.ploID
                    and pr.programID = p.program_id
                    and pr.programID = '{}'
                    GROUP BY p.ploID, r.student_id) derived
             GROUP BY derived.PLOID
                   '''.format(program))
        row = cursor.fetchall()

    return row


# 1c: A table showing the PLOs achieved and failed to achieve (with percentage score) for a selected student in all the courses taken by that student so far.
def getCourseWiseStudentPLO(studentID, cat):
    with connection.cursor() as cursor:
        cursor.execute('''
               SELECT p.ploNum as ploNum,c.courseID, (sum(e.obtainedMarks)/sum(a.totalMarks))*100, derived.Total
               FROM spmapp_registration_t r,
                   spmapp_assessment_t a,
                   spmapp_evaluation_t e,
                   spmapp_co_t co,
                   spmapp_plo_t p,
                   spmapp_course_t c,
                   (
                        SELECT p.ploNum as ploNum,sum(a.totalMarks) as Total, r.student_id as StudentID
                        FROM spmapp_registration_t r,
                            spmapp_assessment_t a,
                            spmapp_evaluation_t e,
                            spmapp_co_t co,
                            spmapp_plo_t p
                        WHERE r.regID = e.reg_id
                            and e.assessment_id = a.assessmentID
                            and a.coID_id=co.coID
                            and co.plo_id = p.ploID
                            and r.student_id = '{}'
                        GROUP BY  r.student_id,p.ploID) derived
               WHERE r.student_id = derived.StudentID
                    and e.reg_id = r.regID
                    and e.assessment_id = a.assessmentID
                    and a.coID_id=co.coID
                    and co.plo_id = p.ploID
                    and p.ploNum = derived.ploNum
                    and c.courseNum = co.course_id

               GROUP BY  p.ploID,co.course_id

               '''.format(studentID))
        row = cursor.fetchall()

    table = []
    courses = []

    for entry in row:
        if entry[1] not in courses:
            courses.append(entry[1])
    courses.sort()
    plo = ["PLO1", "PLO2", "PLO3", "PLO4", "PLO5", "PLO6",
           "PLO7", "PLO8", "PLO9", "PLO10", "PLO11", "PLO12"]

    for i in courses:
        temptable = []
        if cat == 'report':
            temptable = [i]

        for j in plo:
            found = False
            for k in row:
                if j == k[0] and i == k[1]:
                    if cat == 'report':
                        temptable.append(np.round(100 * k[2] / k[3], 2))
                    elif cat == 'chart':
                        temptable.append(np.round(100 * k[2] / k[4], 2))
                    found = True
            if not found:
                if cat == 'report':
                    temptable.append('N/A')
                elif cat == 'chart':
                    temptable.append(0)
        table.append(temptable)
    return plo, courses, table


# ******************* PLO performance trend of selected course/s *************************
# 2a: For chosen semester/s, a chart comparing the PLO achieved percentage for each PLO among the instructors who have taken the course.

def getInstructorWisePLOForCourse(course, semester, uni):
    cursor = connection.cursor()
    cursor.execute('''
        SELECT p.ploNum, COUNT(*)
        FROM
            spmapp_program_t pr,
            spmapp_course_t cr,
            spmapp_section_t sec,
            spmapp_registration_t r,
            spmapp_plo_t p,
            spmapp_co_t c,
            spmapp_department_t d,
            spmapp_school_t sch,
            spmapp_university_t u
        WHERE c.plo_id = p.ploID
            and c.course_id = cr.courseNum
            and cr.courseNum = sec.course_id
            and sec.sectionID = r.section_id
            and p.program_id = pr.programID
            and pr.department_id = d.departmentNum
            and d.school_id = sch.schoolNum
            and sch.university_id = u.universityID
            and cr.courseID = '{}'
            and sec.sec_semester = '{}'
            and u.universityID = '{}'
        GROUP BY p.ploNum

    '''.format(course, semester, uni))

    row1 = cursor.fetchall()
    row1.sort(key=lambda t: len(t[0]))

    cursor.execute('''
            SELECT derived.ins, derived.ploNum, COUNT(*)
            FROM(
                SELECT p.ploNum as ploNum, i.name as ins, 100*(sum(e.obtainedMarks)/sum(a.totalMarks))
                FROM spmapp_registration_t r,
                spmapp_program_t pr,
                spmapp_evaluation_t e,
                spmapp_assessment_t a,
                spmapp_co_t c,
                spmapp_instructor_t i,
                spmapp_plo_t p,
                spmapp_course_t cr,
                spmapp_section_t sec,
                spmapp_department_t d,
                spmapp_school_t sch,
                spmapp_university_t u
            WHERE e.reg_id = r.regID
                and a.assessmentID = e.assessment_id
                and c.course_id = cr.courseNum
                and cr.courseNum = sec.course_id
                and sec.instructor_id = i.instructorID
                and sec.sectionID = r.section_id
                and a.coID_id = c.coID
                and c.plo_id = p.ploID
                and p.program_id = pr.programID
                and pr.department_id = d.departmentNum
                and d.school_id = sch.schoolNum
                and sch.university_id = u.universityID
                and cr.courseID = '{}'
                and sec.sec_semester = '{}'
                and u.universityID = '{}'
                GROUP BY  i.instructorID, p.ploNum,r.student_id
                HAVING  100*(sum(e.obtainedMarks)/sum(a.totalMarks))>=40) derived
            GROUP BY  derived.ins, derived.ploNum
            ORDER BY derived.ins, derived.ploNum
        '''.format(course, semester, uni))

    row2 = cursor.fetchall()
    row2.sort(key=lambda t: len(t[1]))

    plo = []
    fac = []
    table = []

    for i in row1:
        total = i[1]

    for r in row2:
        if r[0] not in fac:
            fac.append(r[0])
        if r[1] not in plo:
            plo.append(r[1])

    for f in fac:
        p = []
        for r in row2:
            if r[0] == f:
                p.append((r[2]/total)*100)
        table.append(p)

    return plo, fac, table


# 2b: For selected PLO/s, within the timeframe of chosen semester/s, a comparison of PLO achievement percentage
# among courses which have the same PLO/s that was/were selected.

def getCourseWisePLOC(course, semester, plo):
    cursor = connection.cursor()

    cursor.execute('''
        SELECT  ploNum, COUNT(*)
        FROM(
            SELECT p.ploNum as ploNum,100*sum(e.obtainedMarks)/sum(a.totalMarks) as marks
            FROM spmapp_registration_t r,
                spmapp_evaluation_t e,
                spmapp_assessment_t a,
                spmapp_co_t c,
                spmapp_course_t cr,
                spmapp_plo_t p
            WHERE r.regID = e.reg_id
                and e.assessment_id = a.assessmentID
                and a.coID_id = c.coID
                and c.plo_id = p.ploID
                and c.course_id = cr.courseNum
                and cr.courseID = '{}'
                and r.reg_semester ='{}'
                and p.ploNum = '{}'
            GROUP BY p.ploNum,r.student_id) derived1
        GROUP BY ploNum

    '''.format(course, semester, plo))

    temp1 = cursor.fetchall()
    temp1.sort(key=lambda t: len(t[0]))

    cursor.execute('''
           SELECT ploNum, COUNT(*)
           FROM(
               SELECT p.ploNum as ploNum,100*sum(e.obtainedMarks)/sum(a.totalMarks) as marks
               FROM spmapp_registration_t r,
                spmapp_evaluation_t e,
                spmapp_assessment_t a,
                spmapp_co_t c,
                spmapp_course_t cr,
                spmapp_plo_t p
               WHERE r.regID = e.reg_id
                and e.assessment_id = a.assessmentID
                and a.coID_id = c.coID
                and c.plo_id = p.ploID
                and c.course_id = cr.courseNum
                and cr.courseID = '{}'
                and r.reg_semester ='{}'
                and p.ploNum = '{}'
               GROUP BY p.ploNum,r.student_id
               HAVING 100*sum(e.obtainedMarks)/sum(a.totalMarks)>=40) derived1
           GROUP BY ploNum
       '''.format(course, semester, plo))

    temp2 = cursor.fetchall()
    temp2.sort(key=lambda t: len(t[0]))
    tt = []
    tt2 = []
    for t in temp1:
        tt.append(t[1])
    for t in temp2:
        tt2.append(t[1])

    return tt2, tt


# 2c: For chosen semester/s, a chart showing the percentage of students who achieved each of the PLOs and
# that of those who failed in a selected course
def getCourseWisePLOComp(course, semester):
    cursor = connection.cursor()
    cursor.execute('''
        SELECT ploNum,COUNT(*)
        FROM(
            SELECT p.ploNum as ploNum, c.course_id, r.student_id, 100*(sum(e.obtainedMarks)/sum(a.totalMarks))
            FROM spmapp_registration_t r,
                spmapp_evaluation_t e,
                spmapp_assessment_t a,
                spmapp_co_t c,
                spmapp_plo_t p,
                spmapp_course_t cr
            WHERE e.reg_id = r.regID
                and a.assessmentID = e.assessment_id
                and a.coID_id = c.coID
                and c.plo_id = p.ploID
                and c.course_id = cr.courseNum
                and cr.courseNum = '{}'
                and r.reg_semester = '{}'
            GROUP BY p.ploNum, c.course_id, r.student_id) derived
        GROUP BY  derived.ploNum

    '''.format(course, semester))

    row1 = cursor.fetchall()
    row1.sort(key=lambda t: len(t[0]))

    cursor.execute('''
            SELECT ploNum,COUNT(*)
            FROM(
                SELECT p.ploNum as ploNum, c.course_id, r.student_id, 100*(sum(e.obtainedMarks)/sum(a.totalMarks))
                FROM spmapp_registration_t r,
                    spmapp_course_t cr,
                    spmapp_evaluation_t e,
                    spmapp_assessment_t a,
                    spmapp_co_t c,
                    spmapp_plo_t p
                WHERE e.reg_id = r.regID
                    and a.assessmentID = e.assessment_id
                    and a.coID_id = c.coID
                    and c.plo_id = p.ploID
                    and c.course_id = cr.courseNum
                    and cr.courseNum = '{}'
                    and r.reg_semester = '{}'
                GROUP BY p.ploNum, c.course_id, r.student_id
                HAVING  100*(sum(e.obtainedMarks)/sum(a.totalMarks))>=40) derived
            GROUP BY  derived.ploNum

        '''.format(course, semester))

    row2 = cursor.fetchall()
    row2.sort(key=lambda t: len(t[0]))

    plo = []
    expected = []
    actual = []

    for r in row1:
        plo.append(r[0])
        expected.append(r[1])

    for r in row2:
        actual.append(r[1])

    return plo, expected, actual


# ******************* PLO performance trend of selected program/s *********************
# 3a: For chosen semester/s, a chart showing the count of students who attempted each PLO against that of those who achieved
# in a selected program/s
def getProgramWisePLOComp(program, semester):
    cursor = connection.cursor()
    cursor.execute('''
        SELECT ploNum,COUNT(*)
        FROM(
            SELECT p.ploNum as ploNum, c.course_id, r.student_id, 100*(sum(e.obtainedMarks)/sum(a.totalMarks))
            FROM spmapp_registration_t r,
                spmapp_program_t pr,
                spmapp_evaluation_t e,
                spmapp_assessment_t a,
                spmapp_co_t c,
                spmapp_plo_t p
            WHERE e.reg_id = r.regID
                and a.assessmentID = e.assessment_id
                and a.coID_id = c.coID
                and c.plo_id = p.ploID
                and p.program_id = pr.programID
                and pr.programID = '{}'
                and r.reg_semester = '{}'
            GROUP BY p.ploNum, c.course_id, r.student_id) derived
        GROUP BY  derived.ploNum

    '''.format(program, semester))

    row1 = cursor.fetchall()
    row1.sort(key=lambda t: len(t[0]))

    cursor.execute('''
            SELECT ploNum,COUNT(*)
            FROM(
                SELECT p.ploNum as ploNum, c.course_id, r.student_id, 100*(sum(e.obtainedMarks)/sum(a.totalMarks))
                FROM spmapp_registration_t r,
                    spmapp_program_t pr,
                    spmapp_evaluation_t e,
                    spmapp_assessment_t a,
                    spmapp_co_t c,
                    spmapp_plo_t p
                WHERE e.reg_id = r.regID
                    and a.assessmentID = e.assessment_id
                    and a.coID_id = c.coID
                    and c.plo_id = p.ploID
                    and p.program_id = pr.programID
                    and pr.programID = '{}'
                    and r.reg_semester = '{}'
                GROUP BY p.ploNum, c.course_id, r.student_id
                HAVING  100*(sum(e.obtainedMarks)/sum(a.totalMarks))>=40) derived
            GROUP BY  derived.ploNum

        '''.format(program, semester))

    row2 = cursor.fetchall()
    row2.sort(key=lambda t: len(t[0]))

    plo = []
    expected = []
    actual = []

    for r in row1:
        plo.append(r[0])
        expected.append(r[1])

    for r in row2:
        actual.append(r[1])

    return plo, expected, actual


# 3b: For chosen semester/s, a chart showing the count of students who achieved each PLO, segmented with color-code into the percentage of the
# count that came from the courses that have that PLO. Alternative view with segmentation based on CO instead of course
# count of student
def getProgramWisePLO(program, cat):
    with connection.cursor() as cursor:
        cursor.execute('''
               SELECT p.ploNum as ploNum,c.courseID, (sum(e.obtainedMarks)/sum(a.totalMarks))*100, derived.Total
               FROM spmapp_registration_t r,
                   spmapp_assessment_t a,
                   spmapp_evaluation_t e,
                   spmapp_co_t co,
                   spmapp_plo_t p,
                   spmapp_course_t c,
                   (
                        SELECT p.ploNum as ploNum,sum(a.totalMarks) as Total, r.student_id as StudentID
                        FROM spmapp_registration_t r,
                            spmapp_assessment_t a,
                            spmapp_evaluation_t e,
                            spmapp_co_t co,
                            spmapp_plo_t p,
                            spmapp_program_t pr
                        WHERE r.regID = e.reg_id
                            and e.assessment_id = a.assessmentID
                            and a.coID_id=co.coID
                            and co.plo_id = p.ploID
                            and p.program_id =  pr.programID
                            and pr.programID = '{}'
                        GROUP BY  r.student_id,p.ploID) derived
               WHERE r.student_id = derived.StudentID
                    and e.reg_id = r.regID
                    and e.assessment_id = a.assessmentID
                    and a.coID_id=co.coID
                    and co.plo_id = p.ploID
                    and p.ploNum = derived.ploNum
                    and c.courseNum = co.course_id
               GROUP BY  p.ploID,co.course_id

               '''.format(program))
        row = cursor.fetchall()

    table = []
    courses = []

    for entry in row:
        if entry[1] not in courses:
            courses.append(entry[1])
    courses.sort()

    plo = ["PLO1", "PLO2", "PLO3", "PLO4", "PLO5", "PLO6",
           "PLO7", "PLO8", "PLO9", "PLO10", "PLO11", "PLO12"]

    for i in courses:
        temptable = []
        # if cat == 'report':
        #     temptable = [i]

        for j in plo:
            found = False
            for k in row:
                if j == k[0] and i == k[1]:
                    # if cat == 'report':
                    #     temptable.append(np.round(100 * k[2] / k[3], 2))
                    temptable.append(np.round(100 * k[2] / k[3], 2))
                    found = True
            if not found:
                # if cat == 'report':
                #     temptable.append('N/A')
                temptable.append(0)
        table.append(temptable)

    return plo, courses, table


def getCOWiseProgramPLO(program, cat):
    with connection.cursor() as cursor:
        cursor.execute('''
               SELECT p.ploNum as ploNum,co.coNum, sum(e.obtainedMarks),sum(a.totalMarks),derived.Total
               FROM spmapp_registration_t r,
                   spmapp_assessment_t a,
                   spmapp_program_t pr,
                   spmapp_evaluation_t e,
                   spmapp_co_t co,
                   spmapp_plo_t p,
                   (
                        SELECT p.ploNum as ploNum,sum(a.totalMarks) as Total, pr.programID as prog
                        FROM spmapp_registration_t r,
                            spmapp_assessment_t a,
                            spmapp_evaluation_t e,
                            spmapp_program_t pr,
                            spmapp_co_t co,
                            spmapp_plo_t p
                        WHERE r.regID = e.reg_id
                            and e.assessment_id = a.assessmentID
                            and a.coID_id=co.coID
                            and co.plo_id = p.ploID
                            and p.program_id = pr.programID
                            and pr.programID = '{}'
                        GROUP BY  r.student_id,p.ploID) derived
               WHERE pr.programID = derived.prog
                    and e.reg_id = r.regID
                    and e.assessment_id = a.assessmentID
                    and a.coID_id=co.coID
                    and co.plo_id = p.ploID
                    and p.ploNum = derived.ploNum
                    and p.program_id = pr.programID

               GROUP BY  p.ploID,co.coNum;

               '''.format(program))
        row = cursor.fetchall()

    table = []
    cos = []

    for entry in row:
        if entry[1] not in cos:
            cos.append(entry[1])
    cos.sort()
    plo = ["PLO1", "PLO2", "PLO3", "PLO4", "PLO5", "PLO6",
           "PLO7", "PLO8", "PLO9", "PLO10", "PLO11", "PLO12"]

    for i in cos:
        temptable = []
        if cat == 'report':
            temptable = [i]

        for j in plo:
            found = False
            for k in row:
                if j == k[0] and i == k[1]:
                    if cat == 'report':
                        temptable.append(np.round(100 * k[2] / k[3], 2))
                    elif cat == 'chart':
                        temptable.append(np.round(100 * k[2] / k[3], 2))
                    found = True
            if not found:
                if cat == 'report':
                    temptable.append('N/A')
                elif cat == 'chart':
                    temptable.append(0)
        table.append(temptable)
    return plo, cos, table


# 3c: Upon clicking on any one of the PLOs from the previous chart, a pie chart showing a clearer segmentation should be displayed.


# ******************** PLO performance trend of selected university/s *******************
# 4a: For a selected program, a radar chart showing the PLO achieved count comparison for each PLO within a chosen time frame.

def getUniversityWiseCountStudent_program(semester, program, uni):

    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT ploNum, COUNT(*)
            FROM(
                SELECT p.ploNum as ploNum, c.course_id, r.student_id, 100*(sum(e.obtainedMarks)/sum(a.totalMarks))
                FROM spmapp_registration_t r,
                    spmapp_program_t pr,
                    spmapp_evaluation_t e,
                    spmapp_assessment_t a,
                    spmapp_co_t c,
                    spmapp_plo_t p,
                    spmapp_department_t d,
                    spmapp_school_t sch,
                    spmapp_university_t u
                WHERE e.reg_id=r.regID
                    and a.assessmentID=e.assessment_id
                    and a.coID_id=c.coID
                    and c.plo_id=p.ploID
                    and p.program_id=pr.programID
                    and pr.department_id=d.departmentNum
                    and d.school_id=sch.schoolNum
                    and sch.university_id=u.universityID
                    and pr.programName='{}'
                    and r.reg_semester='{}'
                    and u.universityID='{}'
                GROUP BY p.ploNum, c.course_id, r.student_id
                HAVING  100*(sum(e.obtainedMarks)/sum(a.totalMarks)) >= 40) derived
            GROUP BY  derived.ploNum

            '''.format(program, semester, uni))

        row1 = cursor.fetchall()

    row1.sort(key=lambda t: len(t[0]))

    plo = []
    actual = []
    total = []
    for r in row1:
        total.append(r[1])

    for r in row1:
        plo.append(r[0])
        actual.append(r[1])

    return plo, actual


# 4b For chosen programs, a radar chart comparing the percentage of graduates who have achieved all PLOs of the chosen programs
# count of student
def getUniversityWiseGraduateStudent(program, uni):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT ploNum, COUNT(*)
            FROM(
                SELECT p.ploNum as ploNum, c.course_id, r.student_id, 100*(sum(e.obtainedMarks)/sum(a.totalMarks))
                FROM spmapp_registration_t r,
                    spmapp_program_t pr,
                    spmapp_evaluation_t e,
                    spmapp_assessment_t a,
                    spmapp_co_t c,
                    spmapp_plo_t p,
                    spmapp_department_t d,
                    spmapp_school_t sch,
                    spmapp_university_t u,
                    spmapp_student_t st
                WHERE e.reg_id=r.regID
                    and a.assessmentID=e.assessment_id
                    and a.coID_id=c.coID
                    and c.plo_id=p.ploID
                    and p.program_id=pr.programID
                    and pr.department_id=d.departmentNum
                    and d.school_id=sch.schoolNum
                    and sch.university_id=u.universityID
                    and pr.programID='{}'
                    and u.universityID='{}'
                    and st.graduateDate IS NOT NULL
                    and st.studentID = r.student_id
                GROUP BY p.ploNum, c.course_id, r.student_id
                HAVING  100*(sum(e.obtainedMarks)/sum(a.totalMarks)) >= 40) derived
            GROUP BY  derived.ploNum

            '''.format(program, uni))

        row1 = cursor.fetchall()

    row1.sort(key=lambda t: len(t[0]))

    plo = []
    actual = []
    total = []
    for r in row1:
        total.append(r[1])

    for r in row1:
        plo.append(r[0])
        actual.append(r[1])

    return plo, actual


# 4c: For a selection of one/more PLO/s, a comparison of the percentage of students who achieved that/those chosen PLO/s (percentage derived from
# total attempted vs achieved)

def getUniversityWisePloPerformance(p, uni):
    cursor = connection.cursor()
    cursor.execute('''
        SELECT ploNum,COUNT(*)
        FROM(
            SELECT p.ploNum as ploNum, c.course_id, r.student_id, 100*(sum(e.obtainedMarks)/sum(a.totalMarks))
            FROM spmapp_registration_t r,
                spmapp_program_t pr,
                spmapp_evaluation_t e,
                spmapp_assessment_t a,
                spmapp_co_t c,
                spmapp_plo_t p,
                spmapp_department_t d,
                spmapp_school_t sch,
                spmapp_university_t u
            WHERE e.reg_id = r.regID
                and a.assessmentID = e.assessment_id
                and a.coID_id = c.coID
                and c.plo_id = p.ploID
                and p.program_id = pr.programID
                and pr.department_id = d.departmentNum
                and d.school_id = sch.schoolNum
                and sch.university_id = u.universityID
                and p.ploNum = '{}'
                and u.universityID = '{}'
            GROUP BY p.ploNum, c.course_id, r.student_id) derived
        GROUP BY  derived.ploNum

    '''.format(p, uni))

    row1 = cursor.fetchall()
    row1.sort(key=lambda t: len(t[0]))

    cursor.execute('''
            SELECT ploNum,COUNT(*)
            FROM(
                SELECT p.ploNum as ploNum, c.course_id, r.student_id, 100*(sum(e.obtainedMarks)/sum(a.totalMarks))
                FROM spmapp_registration_t r,
                spmapp_program_t pr,
                spmapp_evaluation_t e,
                spmapp_assessment_t a,
                spmapp_co_t c,
                spmapp_plo_t p,
                spmapp_department_t d,
                spmapp_school_t sch,
                spmapp_university_t u
            WHERE e.reg_id = r.regID
                and a.assessmentID = e.assessment_id
                and a.coID_id = c.coID
                and c.plo_id = p.ploID
                and p.program_id = pr.programID
                and pr.department_id = d.departmentNum
                and d.school_id = sch.schoolNum
                and sch.university_id = u.universityID
                and p.ploNum = '{}'
                and u.universityID = '{}'
                GROUP BY p.ploNum, c.course_id, r.student_id
                HAVING  100*(sum(e.obtainedMarks)/sum(a.totalMarks))>=40) derived
            GROUP BY  derived.ploNum

        '''.format(p, uni))

    row2 = cursor.fetchall()
    row2.sort(key=lambda t: len(t[0]))

    plo = []
    expected = []
    actual = []

    for r in row1:
        plo.append(r[0])
        expected.append(r[1])

    for r in row2:
        actual.append(r[1])

    return plo, expected, actual


# ****************** Miscellaneous PLO performance trend *******************
# For selected departments/schools, a chart comparing the percentage count of students who achieved all the PLOs they have attempted within a
# chosen time frame.

def getDepartmentWisePLO(department, semester, year):
    with connection.cursor() as cursor:
        cursor.execute(''' 
            SELECT plo.ploNum, c.courseID, st.accountID, (sum(e.obtainedMarks)/sum(a.totalMarks))*100, d.departmentID, sch.schoolID
            FROM spmapp_course_t c,
                spmapp_assessment_t a,
                spmapp_evaluation_t e,    
                spmapp_co_t co,
                spmapp_plo_t plo,
                spmapp_section_t s,
                spmapp_registration_t r,
                spmapp_program_t p,
                spmapp_department_t d,
                spmapp_student_t st,
                spmapp_school_t sch

            WHERE e.assessmentID = a.assessmentID
                and a.coID = co.coID
                and co.courseID = c.courseID
                and co.ploID = plo.ploID
                and s.courseID = c.courseID
                and r.regID = e.regID
                and s.sectionID = r.sectionID
                and p.programID = plo.programID
                and p.departmentID = d.departmentID
                and st.accountID = r.studentID
                and sch.schoolID = d.schoolID
                and d.departmentID = '{}'
                and s.sec_semester = '{}'
                and s.year = '{}'
            GROUP BY plo.ploNum, c.courseID, st.accountID
                '''.format(department, semester, year))
        row = cursor.fetchall()
    return row

 # For selected departments/schools, a chart comparing the average count of PLOs achieved within a chosen time frame. => prev sql
# For a selected instructor, a chart showing the percentage of students who achieved each PLO in the course/s taught by that instructor within a
# chosen time frame. Upon selecting a specific PLO from that chart, a further comparison of PLO achievement percentage w.r.t. other instructors for that
# chosen PLO should be displayed within the same time frame that was already selected for the source chart.


def getInstructorWisePLO(instructor, semester, year):
    with connection.cursor() as cursor:
        cursor.execute(''' 
            SELECT plo.ploNum, c.courseID, r.studentID, (sum(e.obtainedMarks)/sum(a.totalMarks))*100, i.name
            FROM spmapp_course_t c,
                spmapp_assessment_t a,
                spmapp_evaluation_t e,    
                spmapp_co_t co,
                spmapp_plo_t plo,
                spmapp_section_t s,
                spmapp_registration_t r,
                spmapp_instructor_t i

            WHERE e.assessmentID = a.assessmentID
                and a.coID = co.coID
                and co.courseID = c.courseID
                and co.ploID = plo.ploID
                and s.courseID = c.courseID
                and r.regID = e.regID
                and s.sectionID = r.sectionID
                and s.instructorID = i.instructorID
                and i.name = '{}'
                and s.sec_semester = '{}'
                and s.year = '{}'
            GROUP BY plo.ploNum, c.courseID, st.accountID
                '''.format(instructor, semester, year))
        row = cursor.fetchall()
    return row
