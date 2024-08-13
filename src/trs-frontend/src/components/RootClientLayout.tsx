'use client';

import NextAuthProvider from "@/provider/NextauthProvider";
import ReduxProvider from "@/provider/ReduxProvider";


export default function RootClientLayout({ children }: { children: React.ReactNode}) {
    return (
        <NextAuthProvider>
          <ReduxProvider>
            {children}
          </ReduxProvider>
        </NextAuthProvider>
    );
}
