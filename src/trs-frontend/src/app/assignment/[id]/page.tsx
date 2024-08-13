'use client';
import { useParams } from "next/navigation";
import { Spin, Table, Empty, Button } from "antd";
import { ColumnsType } from "antd/es/table";
import Link from "next/link";
import Image from "next/image";
import { ICONS } from "@/config";
import { useEffect, useState } from "react";
import UploadPopup from "./components/UploadPopup";
import { SubmissionStudentRES } from "@/redux/apis/common/submission/submission.response";
import { useCheckRole } from "@/hooks/useCheckRole";
import { useGetSubmissionsQuery } from "@/redux/apis/common/submission/submission.api";

// const data: Array<SubmissionStudentRES> = [
//   {
//     id: 1,
//     status: 'COMPLETE',
//     createdAt: '2024-01-01T00:00:00Z',
//     updatedAt: '2024-01-01T00:00:00Z',
//     score: 120,
//   },
//   {
//     id: 2,
//     status: 'COMPLETE',
//     createdAt: '2024-01-01T00:00:00Z',
//     updatedAt: '2024-01-01T00:00:00Z',
//     score: 120,
//   },
//   {
//     id: 3,
//     status: 'COMPLETE',
//     createdAt: '2024-01-01T00:00:00Z',
//     updatedAt: '2024-01-01T00:00:00Z',
//     score: 120,
//   },
//   {
//     id: 3,
//     status: 'COMPLETE',
//     createdAt: '2024-01-01T00:00:00Z',
//     updatedAt: '2024-01-01T00:00:00Z',
//     score: 120,
//   },
//   {
//     id: 3,
//     status: 'COMPLETE',
//     createdAt: '2024-01-01T00:00:00Z',
//     updatedAt: '2024-01-01T00:00:00Z',
//     score: 120,
//   },
//   {
//     id: 3,
//     status: 'COMPLETE',
//     createdAt: '2024-01-01T00:00:00Z',
//     updatedAt: '2024-01-01T00:00:00Z',
//     score: 120,
//   },
//   {
//     id: 3,
//     status: 'COMPLETE',
//     createdAt: '2024-01-01T00:00:00Z',
//     updatedAt: '2024-01-01T00:00:00Z',
//     score: 120,
//   },
// ];

export default function AssignmentDetail() {
  const { id } = useParams();
  const [isPopupOpen, setIsPopupOpen] = useState(false);
  const togglePopup = () => {
    setIsPopupOpen(!isPopupOpen);
  };

  const { isStudent } = useCheckRole();
  const { data, isFetching, refetch } = useGetSubmissionsQuery({assignment_id: id},{
    skip: !(isStudent),
    refetchOnMountOrArgChange: true,
  });

  useEffect(() => {
    if (isPopupOpen) {
      refetch();
    }
  }, [isPopupOpen, refetch]);

  function getStatus(item: string) {
    if (item == 'WAITING')
      return 'Đang chấm bài';
    else if(item == 'SUCCESS')
      return 'Chấm bài thành công'
    return 'Chấm bài lỗi'
  }

  const columns: ColumnsType<SubmissionStudentRES> = [
    {
      title: (<h1 className="text-center">Lần làm bài</h1>),
      dataIndex: 'index',
      render: (_,record: SubmissionStudentRES) => (
        <div className="">
          <p className="text-center">{record.index + 1}</p>
        </div>
      ),
    },
    {
      title: <p className="text-center">Tình trạng</p>,
      render: (_, record: SubmissionStudentRES) => (
        <div>
          <p>{getStatus(record.status)}</p>
          <p>Cập nhật: {record.updated_at}</p>
        </div>
      ),
    },
    {
      title: <p className="text-center">Mức độ đạt được</p>,
      render: (_, record: SubmissionStudentRES) => (
        <p className="text-center">{record.status == 'WAITING' ? 'từ từ bn êi' : record.scores}</p>
      )
    },
    {
      title: <p className="text-center">Xem lại</p>,
      render: (_, record: SubmissionStudentRES) => (
        <Link
          href={`${id}/recommendation/${record.id}`}
        >
          <p className="text-center underline">Xem lại</p>
        </Link>
      ),
    }
  ];

  return (
    <div>
      <Button
        className="flex flex-row items-center p-10 bg-[#C3FFCB] rounded-10"
        onClick={togglePopup}
      >
        {/* <Image/> */}
        <Image
          src={ICONS.upload}
          alt='upload'
        />
        <div className="flex items-center pl-3">
          <p className="font-semibold text-xl">Tạo lần nộp bài mới</p>
        </div>
      </Button>
      <div className="items-center">
        { data && data.data.length > 0 ? (
          <Spin spinning={isFetching}>
            <div className='mt-0 border-g13 only-border-bottom lg:mt-10'></div>
            <Table
              dataSource={data.data}
              columns={columns}
              scroll={{ x: 700 }}
              pagination={{
                position: ['bottomCenter'],
                responsive: true,
              }}
            />
          </Spin>
        ): (
          <Empty
            className='mt-20 text-sm text-gray-400 flex flex-col items-center justify-center'
            description='Không có dữ liệu.'
          >
          </Empty>
        )}
      </div>
      {isPopupOpen && <UploadPopup id={id as string} onClose={togglePopup}/>}
    </div>
  );
}

