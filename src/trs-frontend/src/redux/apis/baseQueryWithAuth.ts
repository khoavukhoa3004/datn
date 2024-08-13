import { fetchBaseQuery } from '@reduxjs/toolkit/query';
import type { BaseQueryApi, BaseQueryFn, FetchArgs, FetchBaseQueryError } from '@reduxjs/toolkit/query';
import { signOut } from 'next-auth/react';

type MaybePromise<T> = T | Promise<T>;

type FetchBaseQueryArgs = {
    baseUrl?: string
    prepareHeaders?: (
      headers: Headers,
      api: Pick<
        BaseQueryApi,
        'getState' | 'extra' | 'endpoint' | 'type' | 'forced'
      >,
    ) => MaybePromise<Headers | void>
    fetchFn?: (
      input: RequestInfo,
      init?: RequestInit | undefined,
    ) => Promise<Response>
    paramsSerializer?: (params: Record<string, any>) => string
    isJsonContentType?: (headers: Headers) => boolean
    jsonContentType?: string
    timeout?: number
  } & RequestInit

export const baseQueryWithAuth: (
  option: FetchBaseQueryArgs,
) => BaseQueryFn<string | FetchArgs, unknown, FetchBaseQueryError> =
  (option) => async (args, api, extraOptions) => {
    const result = await fetchBaseQuery(option)(args, api, extraOptions);
    if (result.error && result.error.status === 401 ) {
      signOut({ callbackUrl: '/login'});
    }
    return result;
  };
