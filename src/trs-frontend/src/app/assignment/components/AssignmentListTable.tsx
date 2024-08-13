import { ICONS } from "@/config";
import Link from "next/link";
import Image from 'next/image';
import { useCheckLogin } from "@/hooks/useCheckLogin";
import { useRouter } from '@/helpers/router-events';
import { Button, Spin } from "antd";
import { useState } from "react";
import { useGetAssignmentsQuery } from "@/redux/apis/common/assignment/assignment.api";
import { convertToVietnamTime } from "@/utils/gtm-to-vietnam";
import { useCheckRole } from "@/hooks/useCheckRole";
import { signOut } from "next-auth/react";



export default function AssignmentListTable() {
  const { checkLogin } = useCheckLogin();
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const { isAccount, isStudent, isTeacher } = useCheckRole();
  const { data, isFetching } = useGetAssignmentsQuery({
    skip: !isAccount,
    refetchOnMountOrArgChange: 0,
  });

  const handleLinkClick = (itemId: any) => {
    // Perform your action here
    // Navigate to the specified route
    setIsLoading(false);
    if (isStudent) {
      router.push(`/assignment/${itemId}`);
    } else if (isTeacher) {
      router.push(`/assignment/${itemId}/setting`);
    } else if(!isAccount) {
      signOut({ callbackUrl: '/login' });
    }
  };

  return (
    <div>
      {
        data?.data && data?.data?.length > 0 && data.data.map((item) => {
          return (
            <div key={item.id} className="flex flex-row justify-between border-b-2  border-basic-4 m-3">
              <div>
                <h2 className="pb-3 font-bold">{item.name}</h2>
                <h3 className="font-light mb-3">Tác giả: {item.author_name ? item.author_name : 'Bạn'} | Deadline - {convertToVietnamTime(item.end_date)}</h3>
              </div>
              <Button 
                href={`/assignment/${item.id}`}
                key={item.id}
                onClick={(e)=>{
                  e.preventDefault();
                  setIsLoading(true);
                  checkLogin(() => handleLinkClick(item.id));
                }}
                className="cursor-pointer flex items-center"
              >
                <Image 
                  src={ICONS.arrow_left}
                  key={`image${item.id}`}
                  width={24}
                  height={24}
                  alt='narrowRight'
                  className='w-full px-auto items-center'
                />
              </Button>
              <Spin spinning={isFetching} fullscreen/>
              <Spin spinning={isLoading} fullscreen/>
            </div>
          );
        })
      }
    </div>
  );
}
