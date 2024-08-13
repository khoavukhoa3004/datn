import NextAuth from 'next-auth';

declare module 'next-auth' {
    interface Session {
        user: {
            data: {
                email?: string;
                id?: string;
                name?: string;
                type?: string;
            }
        };
        account?: any;
    }
}