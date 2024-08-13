import * as ExcelJS from 'exceljs';

export type ExcelSheetExtendValue<T> = {
  [K in keyof T]: T[K] extends Array<infer E>
    ? {
        [P in keyof E as `${K & string}${Extract<P, number>}`]: {
          name: `${Extract<P, number>}`;
          width?: number;
          idx: number;
        };
      }
    : { name: string; width?: number; idx: number };
};

export function generateExcelFromText(text: string): Promise<ExcelJS.Workbook> {
    return new Promise((resolve, reject) => {
      try {
        let workBook = new ExcelJS.Workbook();
        eval(text);
        resolve(workBook); // Resolve the Promise with the Blob object
      } catch (error) {
        reject(error); // Reject the Promise if an error occurs
      }
    });
  }

export default generateExcelFromText;