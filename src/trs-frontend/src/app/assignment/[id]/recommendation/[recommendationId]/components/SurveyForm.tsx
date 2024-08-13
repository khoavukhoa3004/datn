import { Checkbox, Input, InputNumber, Spin, message } from 'antd';
import TextArea from 'antd/es/input/TextArea';
import { useState } from 'react';
import { getSession, signOut } from 'next-auth/react';
import { useParams } from 'next/navigation';
import axios from 'axios';
import { useGetLastRecommendationDetailQuery, useGetRecommendationDetailQuery } from '@/redux/apis/common/recommendation/recommendation.api';
import { useCheckRole } from '@/hooks/useCheckRole';
import { CreateFormREQ } from '@/redux/apis/common/form/form.request';
import { useCreateFormMutation } from '@/redux/apis/common/form/form.api';


export default function SurveyForm(){
  const { isStudent } = useCheckRole();
  const { recommendationId } = useParams();
  const [isLoading, setIsLoading] = useState(false);
  const [ usedTestcases, setUsedTestcases] = useState<number[]>([]);
  const [ useOrderedTestcase, setUseOrderedTestcase] = useState<string>('');
  const [ useScore, setUseScore] = useState(0);
  const [feedback, setHaveFeedback] = useState('');
  const [createForm] = useCreateFormMutation();

  const { data, isFetching } = useGetLastRecommendationDetailQuery(recommendationId,{
    skip: !isStudent,
    refetchOnMountOrArgChange: true,
  });

  const handleCheckboxChange = (e: React.ChangeEvent<HTMLInputElement>, id: number) => {
    if (e.target.checked) {
      setUsedTestcases((prevIds) => [...prevIds, id]);
      // setUseOrderedTestcase((prevIds) => (prevIds === '' || !prevIds ? String(id) : prevIds + ', ' + String(id)));
    } else {
      setUsedTestcases((prevIds) => prevIds.filter((checkedId) => checkedId !== id));
    }
  };

  async function handleSubmit(e: any) {
    if(!isStudent){
      signOut({callbackUrl: '/login'});
      message.error('Hết hạn đăng nhập');
    }
    setIsLoading(true);
    e.preventDefault();
    const session = await getSession();

    const verifyUsedTestcases = usedTestcases.filter((item)=> data?.data?.files?.map((e)=>e.id)?.includes(item));
    const verifyUsedOrderedTestcase =  useOrderedTestcase.split(',')
    .map((value) => parseInt(value))
    .filter((value) => !isNaN(value));
    const ids = data?.data?.files ? data?.data?.files.map((item) => item.id) : [];
    for (const item of verifyUsedOrderedTestcase) {
      if (!ids.includes(item)) {
        message.info('List testcase id bạn nhập không đúng!');
        setIsLoading(false);   
        return;
      }
    }
    for (const item of verifyUsedTestcases){
      if(!ids.includes(item)) {
        message.info('List testcase id bạn nhập không đúng!');
        setIsLoading(false);   
      }
    }
    if (verifyUsedTestcases.length <= 0 || verifyUsedOrderedTestcase.length <= 0) {
      message.info('List testcase id khác rỗng!');
      setIsLoading(false);
      return;
    }
    if(useScore<=0 || useScore > 5 || !useScore) {
      message.info('Điểm đánh giá phải là số tự nhiên trong khoảng [1,5]');
      setIsLoading(false);
      return;
    }

    const payload = {
      submission_id: data?.data?.last_submission_id,
      used_testcases: verifyUsedTestcases,
      scores: useScore,
      ordered_testcases: verifyUsedOrderedTestcase,
      feedback: feedback,
    } as CreateFormREQ;

    createForm(payload)
      .unwrap()
      .then(()=> {
        message.success('Submit thành công')
      });
  }
  return (
    <div className='bg-white border rounded-lg px-8 py-6 mx-auto my-8 max-w-2xl'>
      <h1 className="text-2xl text-center font-bold mb-3">PHIẾU KHẢO SÁT</h1>
      <form>
        <div className='p-2'>
          <label htmlFor="used_testcase" className="block mb-2 text-lg font-medium text-gray-900 dark:text-white">Các testcase bạn đã <span className="font-bold">&quot;thật sự&quot;</span> sử dụng của gợi ý này?</label>
          { data?.data?.files?.length &&  data?.data?.files?.length > 0 ? 
          <div className="flex flex-row m-3">
            {data?.data?.files.map((item)=>{
            return (
              <Checkbox 
                key={item.id} 
                className='mr-5'
                onChange={(e: any) => handleCheckboxChange(e, item.id)}
                checked={usedTestcases.includes(item.id)}
              >Testcase {item.id}</Checkbox>
            )
          })}
          </div> : <div>Hệ thống lỗi</div>}          
        </div>
        <div className='p-2'>
          <label htmlFor="ordered_testcase" className="block mb-2 text-lg font-medium text-gray-900 dark:text-white">
            Nhớ lại xem, thứ tự thời gian bạn dành ra để giải các testcase lần lượt là (Các testcase cách nhau bằng dấu &apos;,&apos;)
          </label>
          <div>
            {/* <DraggleBox ids={[]}/> */}
            <Input name='ordered_testcase' value={useOrderedTestcase} onChange={(e) => { setUseOrderedTestcase(e.target.value);}} placeholder="Nhập thứ tự testcase id. VD: 1003,1001" />
          </div>
        </div>
        <div className='p-2'>
          <label htmlFor="level" className="block mb-2 text-lg font-medium text-gray-900 dark:text-white">
            Bạn cảm thấy hài lòng về độ khó của các testcase gợi ý (Chọn từ 1 đến 5. 1 là rất không hài lòng / 5 là rất hài lòng)
          </label>
          <div className='flex flex-row items-center'>
            <InputNumber
              min={1}
              max={5}
              value={useScore}
              onChange={value => {
                setUseScore(value ? value : 1);
              }}
            />
          </div>
        </div>
        <div className='p-2'>
          <label htmlFor="feedback" className="block mb-2 text-lg font-medium text-gray-900 dark:text-white">
            Nếu bạn có góp ý hay thắc mắc gì đừng ngần ngại chia sẻ nè:
            </label>
          <TextArea 
            onChange={(e) => { setHaveFeedback(e.target.value);}}
            rows={5} 
            placeholder="Trải ngiệm hệ thống, mô hình, hay bất cứ thứ gì về bài tập lớn nè " 
          />
        </div>
        <div className='flex justify-center items-end pt-3'>
          { !isLoading &&
            <button type="submit" onClick={handleSubmit} className="text-white bg-gradient-to-r from-blue-500 via-blue-600 to-blue-700 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-blue-300 dark:focus:ring-blue-800 shadow-lg shadow-blue-500/50 dark:shadow-lg dark:shadow-blue-800/80 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2 ">Submit</button>
          /* <button type="reset" onClick={resetForm} className="text-white bg-gray-500 hover:bg-gray-600 focus:ring-4 focus:outline-none focus:ring-gray-300 dark:focus:ring-gray-800 shadow-lg shadow-gray-500/50 dark:shadow-lg dark:shadow-gray-800/80 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2">Clear</button> */
          }
          <Spin spinning={isLoading}/>
          <Spin spinning={isFetching} fullscreen/>
        </div>
      </form>
    </div>
  );
}