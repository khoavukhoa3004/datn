
export type RecommendationStudentRES = {
    last_submission_id: string;
    is_filled: boolean;
    files: TescaseFileRES[];
    status: number;
}

export type TescaseFileRES = {
    id: number;
    events: string;
    expect: string;
}