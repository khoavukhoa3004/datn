'use client';

import { Tabs } from "antd";
import TabPane from "antd/es/tabs/TabPane";
import { useRouter } from "@/helpers/router-events";
import PdfDetail from "./components/PdfDetail";
import ExcelDetail from "./components/ExcelDetail";


const ExtensionDetail = () => {
  const router = useRouter();

  return (
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
      <TabPane tab='Write PDF from PdfMake' key='pdf-detail'>
        <PdfDetail />
      </TabPane>
      <TabPane tab='Write Excel from ExcelJS' key='excel-detail'>
        <ExcelDetail />
      </TabPane>
    </Tabs>
  );
};

export default ExtensionDetail;