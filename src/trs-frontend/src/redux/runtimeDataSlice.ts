// runtimeDataSlice.js
import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  value: null,
};

const runTimeDataSlice = createSlice({
  name: 'runTimeData',
  initialState,
  reducers: {
    setRunTimeDataValue: (state, action) => {
      state.value = action.payload;
    },
  },
});

export const { setRunTimeDataValue } = runTimeDataSlice.actions;
export default runTimeDataSlice.reducer;