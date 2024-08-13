'use client';
import { Button } from "antd";
import Image from "next/image";
import AssignmentListTable from "./components/AssignmentListTable";
import { ICONS } from "@/config";
import { useEffect, useState } from "react";
import CreateAssignmentPopup from "./components/CreateAssignmentPopup";
import { useSession } from "next-auth/react";

export default function Assignment() {
  const [isPopupOpen, setIsPopupOpen] = useState(false);
  const { data: session } = useSession();
  const togglePopup = () => {
    setIsPopupOpen(!isPopupOpen);
  };
  return (
    <div>
      <div className="flex flex-row justify-between mb-3 border-b-2 border-basic-4">
        <div>
          <h1 className="text-2xl font-bold mb-3">BÀI TẬP LỚN CỦA TÔI</h1>
          <h2 className="text-xl font-semibold ">Tổng quan các bài tập lớn</h2>
        </div>
        { session?.user?.data?.type === 'TEACHER' && <Image
          src={ICONS.note}
          width={30}
          height={30}
          alt="Edit Assignment"
          className='cursor-pointer p-1'
          onClick={togglePopup}
        />}

      </div>
      
      <h2 className="text-xl font-medium">HỌC KÌ: CQ_HK222</h2>
      <AssignmentListTable/>
      {isPopupOpen && session?.user?.data?.type === 'TEACHER' && <CreateAssignmentPopup onClose={togglePopup}/>}
    </div>
  );
}
