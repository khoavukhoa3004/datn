import { TAG_TYPES } from '@/utils/constants/api.tagTypes';
import { BaseResponse, ListResponse } from '@/redux/response.type';
import { AssignmentRES } from './assignment.response';
import { accountApi } from '../account.api';
import { CreateTeacherREQ } from './assignment.request';

const assignmentApi = accountApi
  .enhanceEndpoints( { addTagTypes: [TAG_TYPES.ASSIGNMENT] })
  .injectEndpoints({
    endpoints: (build) => ({
      getAssignments: build.query<ListResponse<AssignmentRES>, any>({
        query: () => ({
          url: `/assignments`,
          method: 'GET',
        }),
      }),

      getAssignmentDetail: build.query<BaseResponse<AssignmentRES>, any>({
        query: (id: string) => ({
          url: `/assignments/${id}`,
          method: 'GET',
        }),
      }),
      createTeacher: build.mutation<BaseResponse<any>, CreateTeacherREQ>({
        query: (body) => ({
          url: `/assignments/${body.assignment_id}/collaborators`,
          method: 'POST',
          body: {
            email: body.email,
          },
        })
      }),
    })
  })

export const {
  useGetAssignmentsQuery,
  useGetAssignmentDetailQuery,
  useCreateTeacherMutation,
} = assignmentApi;