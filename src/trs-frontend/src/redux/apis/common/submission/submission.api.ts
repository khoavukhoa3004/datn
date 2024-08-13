import { TAG_TYPES } from '@/utils/constants/api.tagTypes';
import { BaseResponse, ListResponse } from '@/redux/response.type';
import { accountApi } from '../account.api';
import { SubmissionStudentRES } from './submission.response';
import { CreateSubmissionREQ } from './submission.request';

const submissionApi = accountApi
  .enhanceEndpoints( { addTagTypes: [TAG_TYPES.SUBMISSION] })
  .injectEndpoints({
    endpoints: (build) => ({
      getSubmissions: build.query<ListResponse<SubmissionStudentRES>, any>({
        query: (params) => ({
          url: `/submissions`,
          method: 'GET',
          params: params,
        }),
      }),
      createSubmission: build.mutation<BaseResponse<any>, {id: string, body: CreateSubmissionREQ}>({
        query: (data) => ({
          url:`/assignments/${data.id}/submission`,
          method: 'POST',
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          body: data.body,
        }),

        invalidatesTags: [TAG_TYPES.SUBMISSION]
      })
    })
  })

export const {
  useGetSubmissionsQuery,
  useCreateSubmissionMutation,
} = submissionApi;