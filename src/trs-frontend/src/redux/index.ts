import { configureStore } from "@reduxjs/toolkit";
import { accountApi } from "./apis/common/account.api";
import { rtkQueryErrorLogger } from "./errorMiddleware";
import { commonApi } from "./apis/common/common.api";
import runTimeDataReducer from './runtimeDataSlice';

export const store = configureStore({
  reducer: {
    [accountApi.reducerPath]: accountApi.reducer,
    [commonApi.reducerPath]: commonApi.reducer,
    runTimeData: runTimeDataReducer,
  },
  middleware: (getDefaultMiddleware) => 
    getDefaultMiddleware().concat([
      rtkQueryErrorLogger,
      accountApi.middleware,
      commonApi.middleware,
    ]),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
