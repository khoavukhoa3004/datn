import { ICONS } from "@/config/icons";
import { ModelTeacherRES } from "@/redux/apis/common/ model/model.response";
import { Button, Empty, Spin } from "antd";
import Table, { ColumnsType } from "antd/es/table";
import { useEffect, useState } from "react";
import Image from "next/image";

const data: Array<ModelTeacherRES> = [
  {
    day: '1',
    model: {
      id: 1,
      name: 'model.py',
      type: 'RNN',
      updatedAt: '2024-01-01',
    },
    hyperParams: {
      id: 1,
      name: 'hyperparam1.py',
    },
    trainingDetail: {
      loss: '0.23',
      trainSets: '1120',
      testSets: '330',
    },
    status: 'everyday',
    countStudent: 124,
  },
  {
    day: '1',
    model: {
      id: 1,
      name: 'model.py',
      type: 'RNN',
      updatedAt: '2024-01-01',
    },
    hyperParams: {
      id: 1,
      name: 'hyperparam1.py',
    },
    trainingDetail: {
      loss: '0.23',
      trainSets: '1120',
      testSets: '330',
    },
    status: 'everyday',
    countStudent: 124,
  },
  {
    day: '1',
    model: {
      id: 1,
      name: 'model.py',
      type: 'RNN',
      updatedAt: '2024-01-01',
    },
    hyperParams: {
      id: 1,
      name: 'hyperparam1.py',
    },
    trainingDetail: {
      loss: '0.23',
      trainSets: '1120',
      testSets: '330',
    },
    status: 'everyday',
    countStudent: 124,
  }
]

const columns: ColumnsType<ModelTeacherRES> = [
  {
    title: <p className="text-center">Day</p>,
    dataIndex: 'day',
    render: (_, record: ModelTeacherRES) => (
      <p className="text-center">{record.day}</p>
    )
  },
  {
    title: <p className="text-center">File Model</p>,
    dataIndex: 'model',
    render: (_, record: ModelTeacherRES) => (
      <div>
        <p>Name: {record.model.name}</p>
        <p>Type: {record.model.type}</p>
        <p>Last update: {record.model.updatedAt}</p>
        <p>Download: </p>
      </div>
    ),
  },
  {
    title: <p className="text-center">Hyper parameter file</p>,
    dataIndex: 'hyperParams',
    render: (_, record: ModelTeacherRES) => (
      <div>
        <p>Name: {record.hyperParams.name}</p>
        <p>Download: {}</p>
      </div>
    ),
  },
  {
    title: <p className="text-center">Training detail</p>,
    dataIndex: 'trainingDetail',
    render: (_, record: ModelTeacherRES) => (
      <div>
        <p>loss: {record.trainingDetail.loss}</p>
        <p>Train ratio: {record.trainingDetail.trainSets}</p>
        <p>Test ratio: {record.trainingDetail.testSets}</p>
      </div>
    ),
  },
  {
    title: <p className="text-center">Schedule status</p>,
    dataIndex: 'status',
    render: (_, record: ModelTeacherRES) => (
      <p className="text-center">{record.status}</p>
    ),
  },
  {
    title: <p className="text-center">Assign student</p>,
    dataIndex: 'countStudent',
    render: (_, record: ModelTeacherRES) => (
      <div className="flex flex-col justify-center items-center">
        <p>Total student use: 124</p>
        <div className="flex justify-center items-center">
          <Button/>
        </div>
      </div>
    )
  }

];

export default function ModelDetail() {
  const [isFetching, setIsFetching] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsFetching(false);
    }, 3000);
    return () => {
      clearTimeout(timer);
    };
  }, []);

  return (
    <div>
      { data && data.length > 0 ? (
        <Spin spinning={isFetching}>
          <div className='mt-0 border-g13 only-border-bottom lg:mt-10'></div>
          <Table
            dataSource={data}
            columns={columns.map((column) => ({
              ...column,
              className: 'border',
            }))}
            scroll={{ x: 1100 }}
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
    </div>
  )
}