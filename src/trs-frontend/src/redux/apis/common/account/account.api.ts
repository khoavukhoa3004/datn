import { TAG_TYPES } from '@/utils/constants/api.tagTypes';
import { commonApi } from '../common.api';

const siteApi = commonApi
  .enhanceEndpoints( { addTagTypes: [TAG_TYPES.ACCOUNT] })
  .injectEndpoints({
    endpoints: (build) => ({
      signinSocial: build.mutation<
        any,
        { provider: 'google';  account: any}
      >({
        query: ({ provider, account }) => ({
          url: `/accounts/login/google`,
          method: 'POST',
          body: { token: account.id_token },
        }),
        transformResponse: (response, meta, arg)=> ({
          data: response,
          account: arg.account,
        }),
      }),
    })
  })

export const {
  useSigninSocialMutation,
} = siteApi;