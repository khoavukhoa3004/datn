export type AssignmentRES = {
  author_name: string | any;
  author_id: string;
  end_date: string;
  id: string;
  name: string;
  start_date: string;
  description: string;
  student_list: StudentListRES[];
  teacher_list: TeacherListRES[];
};

export type StudentListRES = {
  id: string;
  mssv: string;
  name: string;
};

export type TeacherListRES = {
  id: string;
  name: string;
  is_leader: boolean;
  email: string;
};
