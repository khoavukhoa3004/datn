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
import { generatePdfFromText } from "../helpers/PdfTemplate";

const SAMPLE_CODE = `
const CENTIMET_TO_POINT = 28.346;
tt = {
    pageSize: 'A4',
    pageOrientation: 'portrait', // portrait, landscape
    
    //pageMargins: [left, top, right, bottom]
    pageMargins: [ 1.65 * CENTIMET_TO_POINT, 0.765 * CENTIMET_TO_POINT, 1.34 * CENTIMET_TO_POINT, 1.45 * CENTIMET_TO_POINT ],
    // Header
    content: [
      { text: '국민건강보험법 시행규칙 [별지 제2호서식] <개정 2020. 9. 8>', fontSize: 7},
      { text: ['국민연금 당연적용사업장 해당신고서'],fontSize: 15, margin: [1.42*CENTIMET_TO_POINT, 0, 0, 0], bold: true},
      { text: '건강보험 [ ] 사업장(기관) 적용신고서', margin: [1.42*CENTIMET_TO_POINT, 0, 0, 0], fontSize: 15, bold: true},
      { text: '고용보험 ([ ] 보험관계성립신고서[ ] 보험가입신청서)', margin: [1.42*CENTIMET_TO_POINT, 0, 0, 0], fontSize: 15, bold: true},
      { text: '산재보험 ([ ] 보험관계성립신고서[ ] 보험가입신청서)', margin: [1.42*CENTIMET_TO_POINT, 0, 0, 0], fontSize: 15, bold: true},
      { columns: [
        { text: '※ 유의사항 및 작성방법은 제1쪽 뒷면을 참고하여 주시기 바라며, 색상이 어두운 란은 신청인이 적지 않습니다', fontSize: 7, alignment: 'left',width: '70%'},
        { text: '(제1쪽 앞 면)', alignment: 'right', fontSize: 7, width: '30%', margin: [0, 0, 0.5*CENTIMET_TO_POINT, 0]},
      ]},
      {
        table: {
          headerRows: 1,
          widths: ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
          body: [
            [ 
              { text: '접수번호', colSpan: 2, style: 'cellColor', border: [false, false, false, true]},  // border:  [left, top, right, bottom]
              { text: '', style: 'cellColor', border: [false, false, true, true]}, 
              { text: '접수일', colSpan: 3, style: 'cellColor', boder: [false, false, false, true]},
              { text: '', style: 'cellColor', boder: [false, false, false, true]}, 
              { text: '', style: 'cellColor', boder: [false, false, true, true]}, 
              { text: '처리기간 건강보험ㆍ국민연금 3일고용ㆍ산재보험 5일', colSpan: 5, style: 'cellColor', border: [false, false, false, true]},
              // { text: '', style: 'cellColor', border: [false, false, false, true]}, 
              // { text: '', style: 'cellColor', border: [false, false, false, true]}, 
              // { text: '', style: 'cellColor', border: [false, false, false, true]}, 
              // { text: '', style: 'cellColor', border: [false, false, false, true]},   
            ],
            
          ]
        }
      }
      // {
      //   columns: [
      //     { text: '접수번호', alignment: 'left', width: '20%', style: 'cellColor'},
      //     { text: '접수일--', alignment: 'left', width: '30%', style: 'cellColor'},
      //     { text: '처리기간 건강보험ㆍ국민연금 3일고용ㆍ산재보험 5일', alignment: 'left', width: '50%', style: 'cellColor'},
      //   ]
      // }
    ],
    defaultStyle: {
      font: 'IBMPlexSansKR',
      bold: false,
      fontSize: 7,
    },
    styles: {
      // borderLhs: {
      //   border: [true, true, true, true],
      // },
      cellColor: {
        fillColor: '#F2F2F2',
      },
    },
    language: 'korean',
}
`

export default function PdfDetail(){
  const [pdfData, setPdfData] = useState<Blob>();
  const [pdfUrl, setPdfUrl] = useState<string>();
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

  const handleRenderPDF = async () => {
    const blob = await generatePdfFromText(code);
    setPdfUrl(URL.createObjectURL(blob));
    if(blob !== pdfData) {
      console.log(blob);
      setPdfData(blob);
    }
  };

  useEffect(()=> {
    const timer = setTimeout(() => {
      const fetchPdf = async () => {
        if (code === oldCode) return;
        if(!flag) return;
        try {
          const blob = await generatePdfFromText(code);
          setPdfUrl(URL.createObjectURL(blob));
          if(blob !== pdfData) {
            console.log(blob);
            setPdfData(blob);
            setFlag(false);
          }
        } catch (error) {
          // Handle any errors
          console.error('Error fetching data:', error);
        }
      };
      fetchPdf();
    },2000);
    return () => clearTimeout(timer);
  }, [oldCode, code, pdfData, flag])
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
            onClick={handleRenderPDF}
            className="bg-blue-500 text-white px-4 py-2 rounded items-center m-2"
          >
            Generate
          </button>
        </div>
        <div className="flex w-4/9">
            { pdfUrl ? (<embed src={pdfUrl} width='600px' type="application/pdf" />) : code }
        </div>
      </div>
    </div>
  )
}