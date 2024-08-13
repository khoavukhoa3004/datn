import { ErrorEnum } from '@/types/error/error.enum';
import type { Middleware, MiddlewareAPI } from '@reduxjs/toolkit';
import { isRejectedWithValue } from '@reduxjs/toolkit';
import { message, notification } from 'antd';
import { signOut } from 'next-auth/react';

/**
 * Log a warning and show a toast!
 */
export const rtkQueryErrorLogger: Middleware = (api: MiddlewareAPI) => (next) => (action: any) => {
  if (isRejectedWithValue(action) && action?.payload?.data?.statusCode !== 401) {
    notification.error({
      message: 'Error!',
      description:
        action?.payload?.data?.message && action.payload.data.message in ErrorEnum
          ? ErrorEnum[action.payload.data.message as keyof typeof ErrorEnum]
          : 'An error occured.', // An error occurred.
    });
  } else if (isRejectedWithValue(action) && action?.payload?.data?.statusCode === 401) {
    signOut({ callbackUrl: '/login'});
    message.error('Phiên đăng nhập hết hạn');
  }
  return next(action);
};
