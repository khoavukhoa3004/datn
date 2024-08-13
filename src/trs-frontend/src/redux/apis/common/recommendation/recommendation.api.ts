import { TAG_TYPES } from '@/utils/constants/api.tagTypes';
import { BaseResponse, ListResponse } from '@/redux/response.type';
import { accountApi } from '../account.api';
import { RecommendationStudentRES } from './recommendation.response';

const recommendationApi = accountApi
  .enhanceEndpoints( { addTagTypes: [TAG_TYPES.RECOMMENDATION] })
  .injectEndpoints({
    endpoints: (build) => ({

      getRecommendationDetail: build.query<BaseResponse<RecommendationStudentRES>, any> ({
        query: (id) => ({
          url: `/testcases`,
          method: 'GET',
          params: {submission_id: id},
        }) 
      }),
      getLastRecommendationDetail: build.query<BaseResponse<RecommendationStudentRES>, any> ({
        query: (id) => ({
          url: `/testcases/previous`,
          method: 'GET',
          params: {submission_id: id},
        }) 
      })
      // getAssignments: build.query<BaseResponse>, any>({
      //   query: () => ({
      //     url: `/assignments`,
      //     method: 'GET',
      //   }),
      // }),

      // getAssignmentDetail: build.query<BaseResponse<BaseResponse>, any>({
      //   query: (id: string) => ({
      //     url: `/assignments/${id}`,
      //     method: 'GET',
      //   }),
      // }),
    })
  })

export const {
  useGetRecommendationDetailQuery,
  useGetLastRecommendationDetailQuery,
} = recommendationApi;