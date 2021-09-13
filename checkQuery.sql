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
                    and pr.programID = 2
                    GROUP BY p.ploID, r.student_id) derived
             GROUP BY derived.PLOID;