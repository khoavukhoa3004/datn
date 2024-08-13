import { createApi } from '@reduxjs/toolkit/query/react';
import { baseQueryWithAuth } from '../baseQueryWithAuth';

export const commonApi = createApi({
  reducerPath: 'CommonApi',
  keepUnusedDataFor: 10,
  baseQuery: baseQueryWithAuth({
    baseUrl: `${process.env.NEXT_PUBLIC_API_URL}`,
    async prepareHeaders(headers: Headers) {
      headers.set('ngrok-skip-browser-warning', 'true');
      return headers;
    },
  }),
  endpoints: () => ({}),
});
