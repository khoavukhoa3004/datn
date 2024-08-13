export { default } from 'next-auth/middleware';

export const config = { 
    matcher: [
        '/',
        '/student/:path',
        '/teacher/:path',
    ], 
};
