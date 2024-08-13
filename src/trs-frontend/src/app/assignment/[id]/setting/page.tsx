'use client';
import { Tabs } from "antd";
import TabPane from "antd/es/tabs/TabPane";
import ModelDetail from "./components/ModelDetail";
import StudentDetail from "./components/StudentDetail";
import { useRouter } from "@/helpers/router-events";
import { useCheckRole } from "@/hooks/useCheckRole";
import { useEffect, useState } from "react";
import TeacherDetail from "./components/TeacherDetail";



export default function SettingPage({ params }: { params: { id: string}}) {
  const router = useRouter();
  const [canAccess, setCanAccess] = useState(false);
  const { isTeacher } = useCheckRole();

  useEffect(() => {
    if (isTeacher) {
      setCanAccess(true);
    }
  }, [isTeacher]);

  return (
    <div className="">
      {canAccess && 
        <Tabs
          defaultActiveKey='model'
          size='large'
          tabBarGutter={60}
          className='ml-2'
          indicator={{size: 35, align: "center"}}
          onChange={(key) => {
            router.push(`?tab=${key}`)
          }}
          // tabBarExtraContent={<ExtraComponent/>}
        >
          <TabPane tab='Tổng quan' key='model-detail'>
            <ModelDetail />
          </TabPane>
          <TabPane tab='Danh sách sinh viên' key='student-detail'>
            <StudentDetail />
          </TabPane>
          <TabPane tab='Danh sách giảng viên' key='teacher-detail'>
            <TeacherDetail/>
          </TabPane>
        </Tabs>
      }
    </div>
  )
}