import { ICONS } from "@/config";
import { message } from "antd";
import axios from "axios";
import { getSession } from "next-auth/react";
import Image from "next/image";
import { ChangeEvent, useState } from "react";
import { useRouter } from '@/helpers/router-events';



interface UploadPopupProps {
  id: string;
  onClose: () => void;
  // type: PopupType;
  // onHandleType: (newValue: PopupType) => void;
}

const UploadPopup: React.FC<UploadPopupProps> = ({ id, onClose }) => {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const router = useRouter();

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files || []);
    setSelectedFiles(files);
  }

  async function handleUpload() {
		const session = await getSession();
    const requestData = {
      files: selectedFiles,
    }
    axios.post(`${process.env.NEXT_PUBLIC_API_URL}/assignments/${id}/assign-students`, requestData, {
			headers: {
				'authorization': `Bearer ${session?.account.id_token}`,
				'Content-Type': 'multipart/form-data',
			}
		})
    .then((response: any) => {
      message.success('Đăng ký sinh viên thành công');
      router.refresh();
      onClose();
    })
    .catch((error: any) => {
      console.log(error);
      // notification.error(error);
    })
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
        <input type="file" accept=".csv" onChange={handleFileChange} className="mb-4"/>
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