
import { useParams } from "next/navigation";
import { useGetAssignmentDetailQuery } from "@/redux/apis/common/assignment/assignment.api";
import { useCheckRole } from "@/hooks/useCheckRole";

import { ICONS } from "@/config/icons";
import { Button, Empty, Spin } from "antd";
import Table, { ColumnsType } from "antd/es/table";
import { useEffect, useState } from "react";
import Image from "next/image";
import { StudentListRES } from "@/redux/apis/common/assignment/assignment.response";
import UploadPopup from "./UploadFile";

const columns: ColumnsType<StudentListRES> = [
  {
    title: <p className="text-center">ID</p>,
    dataIndex: 'id',
    render: (_, record: StudentListRES) => (
      <p className="text-center">{record.id}</p>
    )
  },
  {
    title: <p className="text-center">Mã số sinh viên</p>,
    dataIndex: 'MSSV',
    render: (_, record: StudentListRES) => (
        <p className="text-center">{record.mssv}</p>
    ),
  },
  {
    title: <p className="text-center">Tên sinh viên</p>,
    dataIndex: 'hyperParams',
    render: (_, record: StudentListRES) => (
      <p className="text-center">{record.name}</p>
    ),
  },
];

export default function StudentDetail() {
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
          Thêm Sinh viên
        </button>
        { data && data?.data?.student_list?.length > 0 ? (
          <Spin spinning={isFetching}>
            <div className='mt-0 border-g13 only-border-bottom lg:mt-10'></div>
            <Table
              dataSource={data?.data?.student_list}
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
            className='mt-20 text-lg-medium-13'
            description='Không có dữ liệu.'
          />
        )}
        {isPopupOpen && <UploadPopup id={id as string} onClose={togglePopup}/>}
      </div>
    )
}