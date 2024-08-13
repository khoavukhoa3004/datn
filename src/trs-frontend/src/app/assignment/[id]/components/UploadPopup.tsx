import { ICONS } from "@/config";
import { message } from "antd";
import axios from "axios";
import { getSession } from "next-auth/react";
import Image from "next/image";
import { ChangeEvent, useState } from "react";
import { useRouter } from '@/helpers/router-events';
import { useCreateSubmissionMutation } from "@/redux/apis/common/submission/submission.api";
import { CreateSubmissionREQ } from "@/redux/apis/common/submission/submission.request";



interface UploadPopupProps {
  id: string;
  onClose: () => void;
  // type: PopupType;
  // onHandleType: (newValue: PopupType) => void;
}

const UploadPopup: React.FC<UploadPopupProps> = ({ id, onClose }) => {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [createSubmission] = useCreateSubmissionMutation();

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const limitSize = 40 *1024;
    const files = Array.from(event.target.files || []);
    let total = 0;
    files.forEach((file) => { 
      if(!file.name.toLowerCase().endsWith('.cpp') && !file.name.toLowerCase().endsWith('.h')) {
        event.target.value = '';
        message.error('Invalid file format: Must be *.cpp or *.h');
        return;
      }
      total += file.size;
    });
    if (total > limitSize) {
      event.target.value = '';
      message.error('Limited size: 40 KB');
    }
    setSelectedFiles(files);
  }

  async function handleUpload() {
		const session = await getSession();
    const requestData = {
      files: selectedFiles,
    } as CreateSubmissionREQ;
    createSubmission({ id: id, body: requestData})
      .unwrap()
      .then(() => {
        message.success('Tạo lần nộp bài thành công');
        onClose();
      });
    // axios.post(`${process.env.NEXT_PUBLIC_API_URL}/assignments/${id}/submission`, requestData, {
		// 	headers: {
		// 		'authorization': `Bearer ${session?.account.id_token}`,
		// 		'Content-Type': 'multipart/form-data',
		// 	}
		// })
    // .then((response: any) => {
    //   message.success('Tạo lần nộp bài thành công');
    //   window.location.reload();
    //   onClose();
      
    // })
    // .catch((error: any) => {
    //   message.error(String(error));
    //   onClose();
    // })
  };

  return (
    <div className="fixed inset-0 flex justify-center items-center">
      <div className="bg-white rounded p-8 h-1/3 w-1/3 z-10 relative">
        <div className="flex flex-row justify-between items-center pb-8">
          <h2 className="text-2xl">Upload Files</h2>
          <Image
            src={ICONS.clear}
            className="cursor-pointer"
            width={30}
            height={30}
            alt="Close"
            onClick={onClose}
          />
        </div>
        <input type="file" multiple accept=".cpp, .h" onChange={handleFileChange} className="mb-4"/>
        <div className="absolute bottom-0 right-0 flex justify-end pr-8 pb-8">
          <button 
            onClick={handleUpload}
            className="bg-blue-500 text-white px-4 py-2 rounded mr-2"
          >
            Upload
          </button>
          <button 
            onClick={onClose}
            className="bg-gray-300 text-gray-700 px-4 py-2 rounded"
          >
            Cancel
          </button>
        </div>
      </div>
      <div className="fixed inset-0 bg-black opacity-70 z-5"></div>
    </div>
  );
}

export default UploadPopup;