import { createApi } from '@reduxjs/toolkit/query/react';
import { getSession, signOut } from 'next-auth/react';
import { baseQueryWithAuth } from '../baseQueryWithAuth';

export const accountApi = createApi({
  reducerPath: 'AccountApi',
  keepUnusedDataFor: 10,  
  baseQuery: baseQueryWithAuth({
    baseUrl: `${process.env.NEXT_PUBLIC_API_URL}`,
    async prepareHeaders(headers) {
      const token = await getSession();
      if (token) {
        headers.set('authorization', `Bearer ${token.account?.id_token}`);
      }
      headers.set('ngrok-skip-browser-warning', 'true');
      return headers;
    },
  }),
  endpoints: () => ({}),
});
