COPY (
select b2.name as district,
	b1.name as block,
	b.name as cluster,
	s.id as school_code,
	s.name school_name,
	moi.name as moi,
	stu.id as student_id,
	c.gender as gender,
	c.dob as dob,
	mt.name as mother_tongue,
	sg.name || sg.section as class_section,
	assess.name as assessment_name,
	prog.name as programme_name,
	ques.name as question,
	ans."answerGrade" as answergrade
from
	schools_institution as s,
	schools_boundary as b,
	schools_boundary as b1,
	schools_boundary as b2,
	schools_answers_orig as ans,
	schools_question as ques,
	schools_student as stu,
	schools_child as c,
	schools_student_studentgrouprelation as ssg,
	schools_studentgroup as sg,
	schools_assessment as assess,
	schools_programme as prog,
	schools_moi_type as moi,
	schools_moi_type as mt,
	schools_institution_languages as lang
where
	s.boundary_id=b.id
	and b.parent_id=b1.id
	and b1.parent_id=b2.id
	and assess.programme_id=prog.id
	and s.id=lang.institution_id
	and lang.moi_type_id=moi.id
	and s.id=sg.institution_id
	and sg.id=ssg.student_group_id
	and ssg.student_id=stu.id
	and stu.child_id=c.id
	and c.mt_id=mt.id
	and stu.id=ans.student_id
	and ans.question_id=ques.id
	and ques.assessment_id=assess.id
	and assess.id in (70) 
	and ssg.academic_id='102'
	and s.id in (30963,30960,33458,30952,30664,30646,30225,31062,30377,33823,31401,30700,31486)
) TO '/home/megha/misc/assessments/aw_557/ang_102_79.csv' WITH  DELIMITER '|' CSV HEADER; 
