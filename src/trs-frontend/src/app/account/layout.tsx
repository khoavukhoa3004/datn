// 'use client';
import MainFooter from "@/layout/footer";
import MainHeader from "@/layout/header";

export const metadata = {
  title: 'Account Page',
  description: 'Information of user',
};

export default function AccountLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="">
      <MainHeader/>
      <div className="flex flex-row">
        <div className="h-screen w-1/6"></div>
        <div className=" m-2 h-screen w-4/6 bg-white shadow-sm p-10">
        {children}
        </div>
      </div>
      <MainFooter/>
    </div>
  );
}
