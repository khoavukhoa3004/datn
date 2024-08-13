import { useSession } from 'next-auth/react';
import { useCheckLogin } from './useCheckLogin';

export function useCheckRole() {
  const { data: session }: any = useSession();


  const isAccount = (session?.user?.data?.type === 'TEACHER') || (session?.user?.data?.type === 'STUDENT');

  const isTeacher = session && session?.user?.data?.type === 'TEACHER';

  const isStudent = (session &&  session?.user?.data?.type) === 'STUDENT';

  return {
    isAccount,
    isTeacher,
    isStudent,
  };
}
