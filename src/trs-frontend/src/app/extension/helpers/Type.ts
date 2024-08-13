// export type ExcelSheetExtendValue<T> = {
//   [K in keyof T]: T[K] extends Array<infer E>
//     ? {
//         [P in keyof E as `${K & string}${Extract<P, number>}`]: {
//           name: `${Extract<P, number>}`;
//           width?: number;
//           idx: number;
//         };
//       }
//     : { name: string; width?: number; idx: number };
// };
