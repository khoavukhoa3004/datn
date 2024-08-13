
'use client';
import { useCheckRole } from '@/hooks/useCheckRole';
import { useGetAssignmentsQuery } from '@/redux/apis/common/assignment/assignment.api';
import { useSession } from 'next-auth/react';
import Image from "next/image";
import { Button, Spin } from "antd";


import Link from "next/link";

const metadata = [
  {
    courseName: 'KỸ THỤÂT LẬP TRÌNH (CO2003)',
    assignmentNumber: 1,
    name: '3 lần kháng chiến quân mông nguyên',
    id: 1,
  },
  {
    courseName: 'KỸ THỤÂT LẬP TRÌNH (CO2003)',
    assignmentNumber: 2,
    name: '3 lần kháng chiến quân mông nguyên 2',
    id: 2,
  },
  {
    courseName: 'KỸ THỤÂT LẬP TRÌNH (CO2003)',
    assignmentNumber: 3,
    name: '3 lần kháng chiến quân mông nguyên 3',
    id: 3,
  },
]
export default function StudentPage() {
  const { data: session } = useSession();
  const { isAccount } = useCheckRole();
  const { data, isFetching } = useGetAssignmentsQuery({
    skip: isAccount,
    refetchOnMountOrArgChange: true,
  });

  return (
    <div>
      <h1 className="text-2xl font-bold mb-3">THÔNG TIN TÀI KHOẢN</h1>
      <div className="flex flex-row items-center  border-basic-5 border-b-2 pb-4">
        <div className='border shadow-xl rounded-full mr-4'>
          <Image 
            src={session?.account?.picture} 
            alt="Profile Image" 
            width={100} 
            height={100}
            className='shadow rounded-full max-w-full h-auto align-middle border-none'
          />
        </div>
        <div className=" border-gray-200">
          <h2 className="text-xl font-medium text-gray-500"><span className="font-medium">Tên: </span>{session?.user?.data?.name}</h2>
          <h2 className="text-xl font-medium text-gray-500"><span className="font-medium">Email: </span>{session?.user?.data?.email}</h2>
        </div>
      </div>

      <h1 className="text-2xl font-bold pt-4 pb-3">DANH SÁCH BÀI TẬP LỚN</h1>
      <div className="border-basic-5 border-b-2 pb-4">
        {data?.data && data?.data?.length > 0 && data.data.map((item) => {
          return (
            <Link 
              key={item.id} 
              className="flex flex-row pb-3"
              href={`/assignment/${item.id}`}
            >
              <p className="underline">{item.name} - Deadline: {item.end_date} - GV: {!item.author_name ? 'Bạn' : item.author_name}</p>
            </Link>
          );
        })}
        <Spin spinning={isFetching} fullscreen/>
      </div>
      
    </div>
  );
}
