'use client';
import { ICONS } from "@/config/icons";
import { Dropdown, Empty, Spin, message } from "antd";
import Table, { ColumnsType } from "antd/es/table";
import Image from "next/image";
import SurveyForm from "./components/SurveyForm";
import { useParams } from "next/navigation";
import axios from 'axios';
import { getSession } from "next-auth/react";
import { useGetLastRecommendationDetailQuery, useGetRecommendationDetailQuery } from "@/redux/apis/common/recommendation/recommendation.api";
import { useCheckRole } from "@/hooks/useCheckRole";
import { TescaseFileRES } from "@/redux/apis/common/recommendation/recommendation.response";
import React from "react";
import { dracula, CodeBlock} from "react-code-blocks"; 


// const data: Array<TestcaseResponse> = [
//   {
//     id: 1,
//     input: `----- file: tc14_input -----
//     172 6 98 1 1
//     19 0
//     ,tc14_aclepius_pack,
//     ----- file: tc14_aclepius_pack -----
//     5
//     5
//     13 14 15 16 17
//     19 18 14 13 15
//     -38 -17 -18 -16 15
//     16 16 16 16 16
//     17 17 17 17 17`,
//     expected: `HP=998, level=1, remedy=0, maidenkiss=0, phoenixdown=0, rescue=-1
//     HP=199, level=1, remedy=0, maidenkiss=0, phoenixdown=0, rescue=-1
//     HP=169, level=1, remedy=0, maidenkiss=0, phoenixdown=0, rescue=-1
//     HP=129, level=1, remedy=0, maidenkiss=0, phoenixdown=0, rescue=-1
//     HP=395, level=1, remedy=0, maidenkiss=0, phoenixdown=0, rescue=1`,
//     got: `HP=395, level=1, remedy=0, maidenkiss=0, phoenixdown=0, rescue=1`,
//   },
//   {
//     id: 1,
//     input: `----- file: tc14_input -----
//     172 6 98 1 1
//     19 0
//     ,tc14_aclepius_pack,
//     ----- file: tc14_aclepius_pack -----
//     5
//     5
//     13 14 15 16 17
//     19 18 14 13 15
//     -38 -17 -18 -16 15
//     16 16 16 16 16
//     17 17 17 17 17`,
//     expected: `HP=998, level=1, remedy=0, maidenkiss=0, phoenixdown=0, rescue=-1
//     HP=199, level=1, remedy=0, maidenkiss=0, phoenixdown=0, rescue=-1
//     HP=169, level=1, remedy=0, maidenkiss=0, phoenixdown=0, rescue=-1
//     HP=129, level=1, remedy=0, maidenkiss=0, phoenixdown=0, rescue=-1
//     HP=395, level=1, remedy=0, maidenkiss=0, phoenixdown=0, rescue=1`,
//     got: `HP=395, level=1, remedy=0, maidenkiss=0, phoenixdown=0, rescue=1`,
//   },
//   {
//     id: 1,
//     input: `----- file: tc14_input -----
//     172 6 98 1 1
//     19 0
//     ,tc14_aclepius_pack,
//     ----- file: tc14_aclepius_pack -----
//     5
//     5
//     13 14 15 16 17
//     19 18 14 13 15
//     -38 -17 -18 -16 15
//     16 16 16 16 16
//     17 17 17 17 17`,
//     expected: `HP=998, level=1, remedy=0, maidenkiss=0, phoenixdown=0, rescue=-1
//     HP=199, level=1, remedy=0, maidenkiss=0, phoenixdown=0, rescue=-1
//     HP=169, level=1, remedy=0, maidenkiss=0, phoenixdown=0, rescue=-1
//     HP=129, level=1, remedy=0, maidenkiss=0, phoenixdown=0, rescue=-1
//     HP=395, level=1, remedy=0, maidenkiss=0, phoenixdown=0, rescue=1`,
//     got: `HP=395, level=1, remedy=0, maidenkiss=0, phoenixdown=0, rescue=1`,
//   }
// ];
const renderData = (text: string | undefined) => {
  if (text === undefined) {
    return '';
  }
  const lines = text.split('\n');
  return lines.map((line, index) => (
    <React.Fragment key={index}>
      {line}
      <br/>
    </React.Fragment>
  ));
}
const columns: ColumnsType<TescaseFileRES> = [
  {
    title: <p className="text-center">Testcase #</p>,
    dataIndex: 'id',
    render: (_, record: TescaseFileRES) => (
      <p className="text-center">{record.id}</p>
    ),
    width: 40,
  },
  {
    title: <p className="text-center">Input</p>,
    dataIndex: 'input',
    // width: '10%',    
    render: (_, record: TescaseFileRES) => (
      <code>{renderData(record.events)}</code>
    ),
  },
  {
    title: <p className="text-center">Expected</p>,
    // width: 150,
    render: (_, record: TescaseFileRES) => (
      <code>{renderData(record.expect)}</code>
    ),
  },
  // {
  //   title: <p className="text-center">Got</p>,
  //   dataIndex: 'got',
  // },
]

export default function RecommendationDetail(){
  const { recommendationId } = useParams();
  const { isStudent } = useCheckRole();
  const { data: PreviousREC, isFetching: isFetchingLastREC } = useGetLastRecommendationDetailQuery(recommendationId, {
    skip: !isStudent,
    refetchOnMountOrArgChange: true,
  })
  const { data, isFetching } = useGetRecommendationDetailQuery(recommendationId,{
    skip: !isStudent || (!PreviousREC?.data?.is_filled),
    refetchOnMountOrArgChange: 5,
  })


  function handleStatus(status: any) {
    switch (status) {
      case 1: {
        return 'Hệ thống đang chấm điểm bài của bạn, vui lòng reload lại trang sau khoảng 3-5 phút';
      }
      case 2: {
        return 'Hệ thống không còn testcases để bạn kiểm tra.'
      }
      case 3: {
        return 'Gợi ý thành công! Dưới đây là một số testcase sai.'
      }
      case 4: {
        return 'Bạn chưa pass hết các testcase sai của lần gợi ý trước.';
      }
      case 5: {
        return 'Đã đạt số lần gợi ý tối đa trong ngày.'
      }
      default:
        return 'Có lỗi gì đó của hệ thống!'
    }
  }

  return (
    <div>
      {  
        PreviousREC && PreviousREC?.data?.files && PreviousREC?.data?.is_filled === false ? (
          <Spin spinning={isFetching}>
            <div>
              <p  className="text-xl font-bold text-red-500"> Đây là tổng kết lại các testcase của lần gợi ý này. Chỉ khi điền phiếu khảo sát xong hệ thống mới sinh gợi ý tiếp.</p>
            </div>
            <div className='mt-0 border-g13 only-border-bottom lg:mt-10'></div>
            <Table
              dataSource={PreviousREC.data.files}
              columns={columns}
              scroll={{ x: 1000 }}
              pagination={{
                position: ['bottomCenter'],
                responsive: true,
              }}
            />
          </Spin>
        ): undefined
      }
      {  
        data && data?.data?.files && PreviousREC?.data?.is_filled === true ? (
          <Spin spinning={isFetching}>
            <div className='mt-1'>
              <h2 className="text-2xl font-bold text-red-500">{handleStatus(data?.data?.status)}</h2>
            </div>
            <div className='mt-0 border-g13 only-border-bottom lg:mt-10'></div>
            <Table
              dataSource={data.data.files}
              columns={columns}
              scroll={{ x: 700 }}
              bordered
              pagination={{
                position: ['bottomCenter'],
                responsive: true,
              }}
            />
          </Spin>
        ): undefined
      }
      {Array<any>(1,2,5,'',undefined).includes(data?.data?.status) && (<div className='mt-20 text-lg-medium-13 items-center'>
        {<h2 className="text-2xl font-bold text-red-500">{data?.message}</h2>}
      </div>)}
      {
        PreviousREC && PreviousREC?.data?.files?.length == 0 && data && data?.data?.files?.length == 0 ?
        (<Empty
          className='mt-20 text-lg-medium-13 items-center'
          description={'Không có dữ liệu.'}
        />) : undefined
      }
      {
        PreviousREC && PreviousREC?.data?.files?.length > 0 && (
          <div>
            <SurveyForm/>
          </div>
        )

      }
      {/* <div>
        <div className='border border-gray-400 rounded'>
          <div className="flex fle-row">
            <Image  src={ICONS.chevron_right} width={20} height={20} alt='chevron'/>
            <p>#</p>
          </div>
          <h2>Input: </h2>
          
        </div>
      </div> */}
    </div>
  );
}
