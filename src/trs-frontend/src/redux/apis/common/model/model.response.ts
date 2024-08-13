


export type ModelTeacherRES = {
  day: string;
  model: {
    id: number;
    name: string;
    type: string;
    updatedAt: string;
  };
  hyperParams: {
    id: number;
    name: string;
  };
  trainingDetail: {
    loss: string;
    trainSets: string;
    testSets: string;
  };
  status: string;
  countStudent: number;
}
