import NextAuth from "next-auth/next";
import GoogleProvider from 'next-auth/providers/google';

const handler = NextAuth({
    secret: process.env.NEXTAUTH_SECRET,
    providers: [
        GoogleProvider({
            clientId: process.env.GOOGLE_CLIENT_ID!,
            clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
        }),
    ],
    session: {
        strategy: 'jwt',
    },
    pages: {
        signIn: '/login',
    },
    callbacks: {
        async session({ session, token }) {
            const { user, account } = token;
            session.user = user as any;
            session.account = account;
            return session;
        },
        async jwt({ token, account, trigger, session }) {
            // console.log('token1', t/oken);
            if (session) {
                token = session;
            }
            if (trigger === 'signIn' && account?.provider === 'google') {
                token.account = { ...account, ...token };
            }
            if (trigger === 'update') {
                // console.log('tokenfa', session);
                token = session;
            }
            return token;
        }
    }
});

export { handler as GET, handler as POST };