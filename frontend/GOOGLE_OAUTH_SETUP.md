# Google OAuth Setup for ZION 2.8.1

## Prerequisites

1. Google Cloud Console account
2. ZION frontend project

## Step 1: Create Google OAuth App

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google+ API" and enable it
4. Create OAuth 2.0 credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client IDs"
   - Choose "Web application"
   - Add authorized redirect URIs:
     - `http://localhost:3007/api/auth/callback/google` (for development)
     - `https://yourdomain.com/api/auth/callback/google` (for production)

## Step 2: Configure Environment Variables

Update your `.env.local` file with the credentials:

```env
# NextAuth Configuration
NEXTAUTH_URL=http://localhost:3007
NEXTAUTH_SECRET=your-super-secret-key-here-generate-random-string

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

## Step 3: Generate NEXTAUTH_SECRET

Run this command to generate a secure secret:

```bash
openssl rand -base64 32
```

Or use an online generator for a random 32-character string.

## Step 4: Test the Setup

1. Start your Next.js development server:
   ```bash
   npm run dev
   ```

2. Visit `http://localhost:3007/dashboard-v2`
3. You should be redirected to the sign-in page
4. Click "Continue with Google"
5. Complete the OAuth flow
6. You should be redirected back to the dashboard

## Troubleshooting

### Common Issues:

1. **"Invalid client" error**:
   - Check that your `GOOGLE_CLIENT_ID` is correct
   - Verify the redirect URI in Google Console matches exactly

2. **"Redirect URI mismatch" error**:
   - Ensure the redirect URI in Google Console includes the full path: `/api/auth/callback/google`
   - Make sure the domain matches (localhost:3007 for development)

3. **Session not persisting**:
   - Check that `NEXTAUTH_SECRET` is set
   - Verify `NEXTAUTH_URL` matches your development URL

### Debug Mode:

Add this to your `.env.local` to enable debug logging:

```env
NEXTAUTH_DEBUG=true
```

## Production Deployment

For production deployment:

1. Update `NEXTAUTH_URL` to your production domain
2. Add production redirect URI to Google Console
3. Use a secure `NEXTAUTH_SECRET`
4. Consider using a database adapter for session storage

## Security Notes

- Never commit `.env.local` to version control
- Use HTTPS in production
- Regularly rotate your `NEXTAUTH_SECRET`
- Monitor OAuth usage in Google Cloud Console

## Next Steps

After successful setup, users can:
- Sign in with their Google account
- Access the WARP Bridge widget
- View their transaction history
- Perform cross-chain transfers

The authentication is now handled securely through Google's OAuth 2.0 flow with JWT tokens managed by NextAuth.js.