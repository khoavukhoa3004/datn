import { ICONS } from "@/config";
import { DatePicker, message } from "antd";
import TextArea from "antd/es/input/TextArea";
import Image from "next/image";
import { useState } from "react";
import axios from 'axios';
import { getSession } from 'next-auth/react';

interface CreateAssignmentProps {
	onClose: () => void;
}
const { RangePicker } = DatePicker;

const CreateAssignmentPopup: React.FC<CreateAssignmentProps> = ({ onClose }) => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [selectedRange, setSelectedRange] = useState<Date[]>([]);
  // const [selectedFile, setSelectedFile] = useState<File | null>(null);
	const [isLoading, setIsLoading] = useState<boolean>(false)

  // const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
  //   const file = event.target.files && event.target.files[0];
  //   if (file) {
  //     setSelectedFile(file);
  //   }
  // };

  async function handleSubmit(){
		const session = await getSession();
		const requestData = {
			name: name,
			description: description,
			// file: selectedFile,
			start_date: selectedRange[0],
			end_date: selectedRange[1],
		}
		axios.post(`${process.env.NEXT_PUBLIC_API_URL}/assignments`, requestData, {
			headers: {
				'authorization': `Bearer ${session?.account.id_token}`,
				'Content-Type': 'application/json',
			}
		})
			.then((response: any) => {
				message.success('Tạo assignment thành công');
				onClose();
			})
			.catch((error: any) => {
				message.error(String(error));
				// notification.error(error);
			})
  };

  return (
    <div className="fixed inset-0 flex justify-center items-center">
      <div className="bg-white rounded p-8 h-[700px] w-1/3 z-10 relative">
        <div className="flex flex-row justify-between items-center pb-8">
          <h2 className="text-2xl font-bold">TẠO BÀI TẬP LỚN MỚI</h2>
          <Image
            src={ICONS.clear}
            className="cursor-pointer"
            width={30}
            height={30}
            alt="Close"
            onClick={onClose}
          />
        </div>
        
				<form> 
					{/* <div className="">
						<label htmlFor="course_name" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Môn học:</label>
						<input 
							type="course_name" 
							id="course_name" 
							className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" 
							placeholder="KỸ THUẬT LẬP TRÌNH" 
							required
						/>
					</div> */}
					<div className="mt-4">
						<label htmlFor="name" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Tên bài tập lớn:</label>
						<input 
							type="assignment_name" 
							id="assignment_name" 
							className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" 
							placeholder="Assignment 1" 
							required
							onChange={(event) => { setName(event.target.value)}}
						/>
					</div>
					
					<div className="mt-4">
						<label 
							htmlFor="timeline" 
							className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
						>
							Chọn timeline:
						</label>
						<RangePicker
							name="timeline"
							required
							onChange={(event) => { 
								if(event[0]?.toDate() && event[1]?.toDate()) {
									setSelectedRange([event[0]?.toDate(), event[1]?.toDate()]);
								}
							}}
						/>
					</div>
					{/* <div className="mt-4">
						<label htmlFor="file"
							className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
						>
							Tải lên danh sách sinh viên
						</label>
						<input type="file" multiple onChange={handleFileChange}/>
					</div> */}
					<div className="mt-4">
						<label htmlFor="description" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Mô tả:</label>
						<TextArea
							name="description"
							placeholder="Enter a description"
							rows={9}
							className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
							onChange={(event) => { setDescription(event.target.value);}}
						/>
					</div>
					<div className="absolute bottom-0 right-0 flex justify-end pr-8 pb-8">
						<button
							type="submit"
							onClick={async(e) => {
								e.preventDefault();
								handleSubmit();
								await new Promise(resolve => setTimeout(resolve, 10000));
								console.log('After suspension');
							}}
							className="bg-blue-500 text-white px-4 py-2 rounded mr-2"
							disabled={isLoading}
						>
							{isLoading ? 'Loading...' : 'Submit'}
						</button>
						<button 
							onClick={onClose}
							className="bg-gray-300 text-gray-700 px-4 py-2 rounded"
						>
							Cancel
						</button>
					</div>
				</form>
      </div>
      <div className="fixed inset-0 bg-black opacity-70 z-5"></div>
    </div>
  );
}

export default CreateAssignmentPopup;