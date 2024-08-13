'use client';
import { IMAGES } from '@/config';
import Image from 'next/image';


export default function MainFooter() {
  return (
    <footer className="h-[200px] relative z-50 flex justify-center items-center text-white text-[18px] bg-[#0d5ca1b0] only-border-top border-g03">
      <div className="absolute inset-0">
        <Image src={IMAGES.footer}
          layout="responsive"
          alt='menu'
          height={250}
          className='flex items-end'
        />
        <div className="bg-blue-500 h-[250px] bg-opacity-40 absolute inset-0 flex justify-center items-center">
          <h1>@TRS - Testcase Recommendation System.</h1>
        </div>
      </div>
    </footer>
  );
}