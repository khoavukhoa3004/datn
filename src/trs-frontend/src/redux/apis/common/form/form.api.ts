import { TAG_TYPES } from '@/utils/constants/api.tagTypes';
import { BaseResponse, ListResponse } from '@/redux/response.type';
import { accountApi } from '../account.api';
import { CreateFormREQ } from './form.request';

const formApi = accountApi
  .enhanceEndpoints( { addTagTypes: [TAG_TYPES.FORM] })
  .injectEndpoints({
    endpoints: (build) => ({
      createForm: build.mutation<BaseResponse<any>, CreateFormREQ>({
        query: (body) => ({
          url: `/forms`,
          method: 'POST',
          params: body,
        }),
        invalidatesTags: [TAG_TYPES.FORM]
      }),
    })
  })

export const {
  useCreateFormMutation,
} = formApi;