import { ICONS } from "@/config";
import { Input, InputNumber, message } from "antd";
import axios from "axios";
import { getSession } from "next-auth/react";
import Image from "next/image";
import { ChangeEvent, useState } from "react";
import { useRouter } from '@/helpers/router-events';
import { useCreateTeacherMutation } from "@/redux/apis/common/assignment/assignment.api";
import { CreateTeacherREQ } from "@/redux/apis/common/assignment/assignment.request";



interface UploadPopupProps {
  id: string;
  onClose: () => void;
}

const CreateTeacherPopup: React.FC<UploadPopupProps> = ({ id, onClose }) => {
  const [email, setEmail] = useState('');
  const router = useRouter();
  const [createTeacher] = useCreateTeacherMutation();

  async function handleCreateTeacher() {
    const payload = {
      assignment_id: id,
      email: email,
    } as CreateTeacherREQ;
    createTeacher(payload)
      .unwrap()
      .then(() => {
        message.success('Đăng ký sinh viên thành công');
        onClose();
      })
  };

  return (
    <div className="fixed inset-0 flex justify-center items-center">
      <div className="bg-white rounded p-8 h-1/3 w-1/3 z-10 relative">
        <div className="flex flex-row justify-between items-center pb-8">
          <h2 className="text-2xl">Thêm giảng viên</h2>
          <Image
            src={ICONS.clear}
            className="cursor-pointer"
            width={30}
            height={30}
            alt="Close"
            onClick={onClose}
          />
        </div>
        <div className='p-2'>
          <label htmlFor="level" className="block mb-2 text-lg font-medium text-gray-900 dark:text-white">
            Email:
          </label>
          <Input placeholder="abcd@hcmut.edu.vn" value={email} onChange={(event) => setEmail(event.target.value)}/>;
        </div>        
        <div className="absolute bottom-0 right-0 flex justify-end pr-8 pb-8">
          <button 
            onClick={handleCreateTeacher}
            className="bg-blue-500 text-white px-4 py-2 rounded mr-2"
          >
            Accept
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

export default CreateTeacherPopup;