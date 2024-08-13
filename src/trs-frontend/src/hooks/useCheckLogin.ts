import { message, notification } from 'antd';
import { signOut, useSession } from 'next-auth/react';
import { useState } from 'react';
import { useRouter } from '@/helpers/router-events';


export function useCheckLogin() {
  const { data: session, update: updateSession }: any = useSession();
  const checkLogin = (handleOK: () => void) => {
    if (session) {
      console.log(session);
      const currentDate = new Date();
      if(session.account?.expires_at && (new Date(session.account?.expires_at*1000) < currentDate)) {
        updateSession({})
        message.error('Hết hạn đăng nhập');
      } else if(!session.account?.expires_at){
        message.error('Invalid session');
        updateSession({});
      }
      if (session.user && (session.user?.data?.type === 'STUDENT' || session.user?.data?.type === 'TEACHER')){
        handleOK();
        return true;      
      } else {
        updateSession({});
      }
      signOut({ callbackUrl: '/login'})
      return false;
    } else {
      notification.info({ message: 'Phiên đăng nhập hết hạn', duration: 4 });
      signOut({ callbackUrl: '/login'})
      return false;
    }
  };

  return {
    checkLogin,
  };
}
