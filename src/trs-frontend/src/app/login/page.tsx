'use client';

import GoolgeLogin from "./components/GoogleLogin";


export default function Login() {

  return (
    <section className="flex items-center justify-center h-screen">
      <div className="w-[62.5vw] max-w-[500px] h-[30vh] max-h=[200px] bg-white shadow-lg rounded-5 flex flex-col items-center justify-center">
        <h1 className="text-3xl font-bold pb-6">LOGIN</h1>
        <GoolgeLogin/>
      </div>
    </section>
  );
}
