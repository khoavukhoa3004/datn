export type BaseResponse<T> = {
    message: string;
    data: T;
};

export type ListResponse<T> = {
    message: string;
    data: T[];
}
