'use client';
import React, { useState, useEffect } from "react";
import CodeMirror, { ViewUpdate } from '@uiw/react-codemirror';
import { markdown, markdownLanguage } from '@codemirror/lang-markdown';
import { javascript } from '@codemirror/lang-javascript';
import { python } from '@codemirror/lang-python';
import { css } from '@codemirror/lang-css';
import { html } from '@codemirror/lang-html';
import { json } from '@codemirror/lang-json';
import { EditorView } from '@codemirror/view';
import { languages } from '@codemirror/language-data';
import generateExcelFromText from "../helpers/ExcelTemplate";
import { SheetsDirective, SheetDirective, RangesDirective, RangeDirective, SpreadsheetComponent } from '@syncfusion/ej2-react-spreadsheet';

const SAMPLE_CODE = `
// Create a new Excel file and download it when the button is clicked.
// For render excel, please use object: workBook (its type: ExcelJS). This is global object i no need to re-defined this object.
// Please write syntax like Typescript
// Sample code: 
  let workSheet = workBook.addWorksheet('List');
  let headers = [
    {
      key: 'code',
      name: 'Index',
      width: 15,
    }, 
    {
      key: 'name',
      name: 'Student Name',
      width: 25,
    },
    {
      key: 'phone',
      name: 'Phone Number',
      width: 25,
    },
  ];
  
  
  workSheet.getRow(1).alignment = { horizontal: 'center' };
  const mergedCell = workSheet.getCell('A1');
  mergedCell.value = "abc";
  console.log(mergedCell.value)
  mergedCell.font = { size: 20, bold: true };
  mergedCell.alignment = { horizontal: 'center', vertical: 'middle' };
  mergedCell.border = { bottom: { style: 'thin' } };
  workSheet.mergeCells('A1:C3');
  const headerRow = workSheet.getRow(3);
  let i = 1;
  for (const header in headers) {
    const cell = headerRow.getCell(i);
    cell.value = header.name;
    cell.border = { top: { style: 'thin' }, left: { style: 'thin' }, bottom: { style: 'thin' }, right: { style: 'thin' } };
    cell.alignment = { horizontal: 'center' };
    const column = workSheet.getColumn(i);
    if (header.width) {
      column.width = header.width;
    }
    i += 1;
  }
`;

export default function ExcelDetail(){
  const [excelData, setExcelData] = useState<Blob>();
  const [excelUrl, setExcelUrl] = useState<string>();
  const [oldCode, setOldCode] = useState<string>('');
  const [code, setCode] = useState<string>(SAMPLE_CODE);
  const [flag, setFlag] = useState<boolean>(false);
  const handleCodeChange = (value: string, viewUpdate: ViewUpdate) => {
    if (value !== code) {
      setOldCode(code);
      setCode(value);
      setFlag(true);
    }
  };

  const handleRenderExcel = async () => {
    const workBook = await generateExcelFromText(code);
    // await workBook.xlsx.load(workBook);
    const excelBuffer = await workBook.xlsx.writeBuffer();
    const blob = new Blob([excelBuffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=UTF-8' });

    if(blob !== excelData) {
      console.log(blob);
      setExcelData(blob);
      setExcelUrl(URL.createObjectURL(blob));
    }
  };

  // useEffect(()=> {
  //   const timer = setTimeout(() => {
  //     const fetchExcel = async () => {
  //       if (code === oldCode) return;
  //       if(!flag) return;
  //       try {
  //         const workBook = await generateExcelFromText(code);
  //         // await workBook.xlsx.load(workBook);
  //         const excelBuffer = await workBook.xlsx.writeBuffer();
  //         const blob = new Blob([excelBuffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });

  //         setExcelUrl(URL.createObjectURL(blob));
  //         if(blob !== excelData) {
  //           console.log(blob);
  //           setExcelData(blob);
  //           setFlag(false);
  //         }
  //         console.log('excel file', URL.createObjectURL(blob));
  //       } catch (error) {
  //         // Handle any errors
  //         console.error('Error fetching data:', error);
  //       }
  //     };
  //     fetchExcel();
  //   },2000);
  //   return () => clearTimeout(timer);
  // }, [oldCode, code, excelData, flag])
  return (
    <div>
      <div className='flex flex-row'>
        <CodeMirror
          className="flex w-4/9"
          value={code}
          height="1000px"
          width="800px"
          editable={true}
          extensions={
            [
            javascript({ jsx: true }),
            markdown({ base: markdownLanguage, codeLanguages: languages }),
            python(),
            css(),
            html(),
            json(),
            EditorView.lineWrapping,
            ]
          }
          onChange={handleCodeChange}
        />
        <div className="flex w-1/9 h-[700px] items-center justify-center">
          {/* <div */}
          <button 
            onClick={handleRenderExcel}
            className="bg-blue-500 text-white px-4 py-2 rounded items-center m-2"
          >
            Generate
          </button>
        </div>
        {/* <div className="flex w-4/9">
            { excelUrl ? (<iframe  src={excelUrl} width="100%" height="600px" type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" />) : code }
        </div> */}
        <div className="flex w-4/9">
            { excelUrl ? (<iframe  src={excelUrl} width="100%" height="600px" />) : code }
        </div>
      </div>
    </div>
  )
}