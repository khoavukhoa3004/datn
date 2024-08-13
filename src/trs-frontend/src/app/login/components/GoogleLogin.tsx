import { signIn, useSession } from 'next-auth/react';
import { Spin, message } from 'antd';
import { useEffect, useState } from 'react';
import { useRouter } from '@/helpers/router-events';
import { useSigninSocialMutation } from '@/redux/apis/common/account/account.api';
import Image from 'next/image';
import { ICONS } from '@/config';


export default function GoolgeLogin({ size = 55 }: { size?: number }) {
  const [verify, setVerify] = useState(false);
  const { data: session, update: updateSession } = useSession();
  const router = useRouter();
  const [signInSocial, { isLoading }] = useSigninSocialMutation();

  useEffect(() => {
    console.log('toi day');
    if (session) {
      const currentDate = new Date();
      if (session?.account && !verify) {
        // call api to verify social token
        if(session.account?.expires_at && (new Date(session.account?.expires_at*1000) < currentDate)) {
          updateSession({})
          message.error('Hết hạn đăng nhập');
          router.replace('/login')
        } else if(!session.account?.expires_at){
          message.error('Invalid session');
          updateSession({});
          router.replace('/login')
        }
        
        setVerify(true);
        const { account } = session;
        console.log('hah', account);
        signInSocial({ provider: account.provider, account: account})
        .unwrap()
        .then((res: any) => {
          console.log('tai day');
          if(res.name === 'HttpException') {
            updateSession({})
            message.error('Không có tài khoản trên hệ thống hah');
            // router.replace('/login')
          } else {
            const sessionOfGoogleLogin = {
              user: res.data,
              account: {
                id_token: res.account.id_token,
                expires_at: res.account.expires_at,
                email: res.account.email,
                provider: 'google',
                token_type: res.account.token_type,
                type: 'oauth',
                picture: res.account.picture,
              },
              expires: session.expires,
            }
            updateSession(sessionOfGoogleLogin).then(()=> {
              message.success('Đăng nhập thành công');
              router.replace('/assignment')
            })
          }
        }).catch((error) => {
          message.error('Không có tài khoản trên hệ thống', error);
          updateSession({});
          router.replace('/login');
        })

      }
      else if (session?.account && verify){
        if(session.account?.expires_at && (new Date(session.account?.expires_at*1000) < currentDate)) {
          updateSession({})
          message.error('Hết hạn đăng nhập');
          router.replace('/login')
        } else if(!session.account?.expires_at){
          message.error('Invalid session');
          updateSession({});
          router.replace('/login')
        }
        if (session.user){
          router.replace('/assignment');
        } else {
          updateSession({});
          router.replace('/login')
        }
      }
    }
  }, [signInSocial, updateSession, session, router, verify]);
  
  return (
    <div className="flex justify-center border-basic-4">
      <div
        key='google'
        className="cursor-pointer flex flex-row bg-basic-4 pl-5 pr-5 pt-2 pb-2 rounded-10" 
        onClick={() => {
          setVerify(false);
          signIn('google', {}, { prompt: 'login'})
        }}
      >
        <Image
              src= {ICONS.google}
              alt= {'google'}
              width={size ? size : 55}
              height={size ? size : 55}
            />
        <h2 className='text-2xl text-black text-opacity-54 font-semibold flex items-center'>Continue with Google</h2>
      </div>
      <Spin spinning={isLoading} fullscreen/>
    </div>
  );
}
