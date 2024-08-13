export type CreateFormREQ = {
  submission_id: string;
  used_testcases: number[];
  scores: number;
  ordered_testcases: number[],
  feedback: string;
};