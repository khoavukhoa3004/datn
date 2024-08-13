'use client';
import { useParams } from "next/navigation";
import { useGetAssignmentDetailQuery } from "@/redux/apis/common/assignment/assignment.api";
import { useCheckRole } from "@/hooks/useCheckRole";
import React, { useState } from "react";
import { Button } from "antd";



export default function Layout({ children }: { children: React.ReactNode }) {
  const { id } = useParams();
  const { isStudent } = useCheckRole();
  const [isExpanded, setIsExpanded] = useState(true);
  const handleToggleExpand = () => {
    setIsExpanded(!isExpanded);
  };
  const { data, isFetching } = useGetAssignmentDetailQuery( id as string,{
    skip: !isStudent,
    refetchOnMountOrArgChange: true,
  });

  const renderData = (text: string | undefined) => {
    if (text === undefined) { 
      return '';
    }
    const lines = text.split('\n');
    const temp = lines.map((line, index) => {
      return (
        <div key={index} className="pb-2">
          {line}
          {/* <br /> */}
        </div>
      );
    });
    return temp;
  }
  return (
    <div className="">
      <div className="border-b-2 border-basic-4 mb-4">
        <h1 className="text-2xl font-bold">KỸ THUẬT LẬP TRÌNH (CO2003) - HỌC KÌ: CQ_HK222</h1>
        <h2 className="text-xl font-medium mt-2">{data?.data?.name}</h2>
      </div>
      <div>
        <p className="text-basic-5 font-semibold pb-2">Closed: {data?.data?.end_date}</p>
        <div className="pb-2">
          <div className="text-basic-6 font-semibold">{isExpanded ? renderData(data?.data?.description) : renderData(data?.data?.description.slice(0, 303))  } </div>
          <button className="text-sm text-basic-4" onClick={handleToggleExpand}>{!isExpanded ? 'Show more' : 'Show less'}</button>
        </div>
        <p className="text-basic-6 font-semibold pb-2">Số lần gợi ý tối đa: 5 lần một ngày. (Sẽ cập nhật hiển thị sau)</p>
      </div>
      {children}

    </div>
  );
}
