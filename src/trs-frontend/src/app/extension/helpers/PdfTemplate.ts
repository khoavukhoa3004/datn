import { ICONS } from "@/config";
import { FONTS } from "@/config/fonts";
import pdfMake from "pdfmake/build/pdfmake";
import pdfFonts from "pdfmake/build/vfs_fonts";
import { TDocumentDefinitions, TFontDictionary, } from 'pdfmake/interfaces';

const customFont: TFontDictionary = {
  Roboto: {
    normal: FONTS.ibm_plex_sans_kr_regular,
    bold:  FONTS.ibm_plex_sans_kr_bold,
  }
}
pdfMake.vfs = pdfFonts.pdfMake.vfs;
pdfMake.vfs["IBMPlexSansKR-Bold.ttf"] = FONTS.ibm_plex_sans_kr_bold;
pdfMake.vfs["IBMPlexSansKR-Regular.ttf"] = FONTS.ibm_plex_sans_kr_regular;
pdfMake.fonts = {
  IBMPlexSansKR: {
    normal: "IBMPlexSansKR-Regular.ttf",
    bold: "IBMPlexSansKR-Bold.ttf",
  }
};

const CENTIMET_TO_POINT = 28.346;
var dd: TDocumentDefinitions = {
    pageSize: 'A4',
    pageOrientation: 'portrait', // portrait, landscape
    
    //pageMargins: [left, top, right, bottom]
    pageMargins: [ 1.65 * CENTIMET_TO_POINT, 0.765 * CENTIMET_TO_POINT, 1.34 * CENTIMET_TO_POINT, 1.45 * CENTIMET_TO_POINT ],
    // Header
    content: [
      { text: `국민건강보험법 시행규칙 [별지 제2호서식] <개정 2020. 9. 8>`, fontSize: 7},
      { text: [`국민연금 [`, {svg: ICONS.chevron_right}, `] 당연적용사업장 해당신고서`],fontSize: 15, margin: [1.42*CENTIMET_TO_POINT, 0, 0, 0], bold: true},
      { text: `건강보험 [ ] 사업장(기관) 적용신고서`, margin: [1.42*CENTIMET_TO_POINT, 0, 0, 0], fontSize: 15, bold: true},
      { text: `고용보험 ([ ] 보험관계성립신고서[ ] 보험가입신청서)`, margin: [1.42*CENTIMET_TO_POINT, 0, 0, 0], fontSize: 15, bold: true},
      { text: `산재보험 ([ ] 보험관계성립신고서[ ] 보험가입신청서)`, margin: [1.42*CENTIMET_TO_POINT, 0, 0, 0], fontSize: 15, bold: true},
      { columns: [
        { text: `※ 유의사항 및 작성방법은 제1쪽 뒷면을 참고하여 주시기 바라며, 색상이 어두운 란은 신청인이 적지 않습니다`, fontSize: 7, alignment: 'left',width: '70%'},
        { text: `(제1쪽 앞 면)`, alignment: 'right', fontSize: 7, width: '30%', margin: [0, 0, 0.5*CENTIMET_TO_POINT, 0]},
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
async function generatePdf(): Promise<Blob> {
  return new Promise((resolve) => {
    const pdfDoc = pdfMake.createPdf(dd,undefined); // Create the PDF document
    pdfDoc.getBlob((result) => {
      resolve(new Blob([result], { type: 'application/pdf' })); // Resolve the promise with the Blob object
    });
  });
}

export function generatePdfFromText(text: string): Promise<Blob> {
  return new Promise((resolve, reject) => {
    try {
      let tt = {} as TDocumentDefinitions;
      eval(text);
      const pdfDoc = pdfMake.createPdf(tt);
      pdfDoc.getBlob((blob: Blob) => {
        resolve(blob); // Resolve the Promise with the Blob object
      });
    } catch (error) {
      reject(error); // Reject the Promise if an error occurs
    }
  });
}
export default generatePdf;