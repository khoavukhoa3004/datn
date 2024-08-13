
import { useParams } from "next/navigation";
import { useGetAssignmentDetailQuery } from "@/redux/apis/common/assignment/assignment.api";
import { useCheckRole } from "@/hooks/useCheckRole";

import { ICONS } from "@/config/icons";
import { Button, Empty, Spin } from "antd";
import Table, { ColumnsType } from "antd/es/table";
import { useEffect, useState } from "react";
import Image from "next/image";
import { TeacherListRES } from "@/redux/apis/common/assignment/assignment.response";
import CreateTeacherPopup from "./CreateTeacherPopup";

const columns: ColumnsType<TeacherListRES> = [
  {
    title: <p className="text-center">ID</p>,
    dataIndex: 'id',
    render: (_, record: TeacherListRES) => (
      <p className="text-center">{record.id}</p>
    )
  },
  {
    title: <p className="text-center">Tên giảng viên</p>,
    dataIndex: 'name',
    render: (_, record: TeacherListRES) => (
        <p className="text-center">{record.name}</p>
    ),
  },
  {
    title: <p className="text-center">Email</p>,
    dataIndex: 'hyperParams',
    render: (_, record: TeacherListRES) => (
      <p className="text-center">{record.email}</p>
    ),
  },
];

export default function TeacherDetail() {
    const { id } = useParams();
    const { isTeacher } = useCheckRole();
    const [isPopupOpen, setIsPopupOpen] = useState(false);
    const togglePopup = () => {
      setIsPopupOpen(!isPopupOpen);
    };

    const { data, isFetching } = useGetAssignmentDetailQuery( id as string,{
      skip: !isTeacher,
      refetchOnMountOrArgChange: true,
    });
    return (
      <div>
        <button 
          className="bg-blue-500 hover:bg-blue-400 text-white font-bold py-2 px-4 border-b-4 border-blue-700 hover:border-blue-500 rounded"
          onClick={togglePopup}
        >
          Thêm Giảng viên
        </button>
        { data && data?.data?.teacher_list?.length > 0 ? (
          <Spin spinning={isFetching}>
            <div className='mt-0 border-g13 only-border-bottom lg:mt-10'></div>
            <Table
              dataSource={data?.data?.teacher_list}
              columns={columns.map((column) => ({
                ...column,
                className: 'border',
              }))}
              scroll={{ x: 400 }}
              pagination={{
                position: ['bottomCenter'],
                responsive: true,
              }}
            />
          </Spin>
        ): (
          <Empty
            image={<Image src={ICONS.warning} alt='empty' />}
            className='mt-20 text-lg-medium-13 justify-center'
            description='Không có dữ liệu.'
          />
        )}
        {isPopupOpen && <CreateTeacherPopup id={id as string} onClose={togglePopup}/>}
      </div>
    )
}