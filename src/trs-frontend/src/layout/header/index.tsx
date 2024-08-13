'use client';
import { Button, Layout, Spin, message } from 'antd';
import { ICONS, IMAGES } from '@/config';
import Image from 'next/image';
import { useRouter } from '@/helpers/router-events';
import { useSession, signOut } from 'next-auth/react';

const { Header } = Layout;

export default function MainHeader() {
  const router = useRouter();
  const { data: session, status } = useSession();
  
  const logout = () => {
    message.success('Logout success');
    signOut({ callbackUrl: '/login' }); // Clear the session and log the user out
  };

  return (
    <Header className='bg-white flex flex-row items-center justify-center shadow-lg'>
      <Image src={IMAGES.hcmut} 
        width={50}
        height={50}
        alt='menu'
        className='flex items-end'
        onClick={() => { router.replace('/student'); }}
      />
      <h1 className='flex w-1/5 items-center justify-center text-2xl font-semibold'>Trang chủ</h1>
      <div
        className='flex w-1/5 items-center justify-center cursor-pointer'
        onClick={() => {
          router.replace('/assignment')
        }}
      >
        <h1 className='text-gray-500'>BÀI TẬP LỚN CỦA TÔI</h1>
      </div>
      <div
        className='flex w-1/5 items-center justify-center cursor-pointer'
        onClick={() => {
          router.replace('/account')
        }}
      >
        <h1 className='text-gray-500'>TÀI KHOẢN</h1>
      </div>
      <div className='flex w-1/5 items-center justify-center ' >
        <Button 
          onClick={(e) => {
            e.preventDefault();
            logout();
          }}
          className='p-1'
        >
          <Image
            src={ICONS.logout}
            width={25}
            height={25}
            alt='Logout'
            className='p-1'
          />
        </Button>
        <Spin spinning={status === 'loading'} fullscreen/>
      </div>
    </Header>
  );
}