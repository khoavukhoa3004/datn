import React, { useState } from "react";

import { Layout } from "antd";
import MainHeader from "./header";


export default function MainLayout() {
  return (
    <Layout>
      <MainHeader />
    </Layout>
  );
}