"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { LoginForm } from '../components/AuthForms';

export default function LoginPage() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const handleLogin = async (email: string, password: string) => {
    setLoading(true);
    setError(null);

    try {
      // TODO: Implement actual login API call
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        throw new Error('Login failed');
      }

      const data = await response.json();

      // Store JWT token
      localStorage.setItem('zion_auth_token', data.token);

      // Redirect to dashboard
      router.push('/dashboard-v2');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return <LoginForm onLogin={handleLogin} loading={loading} error={error} />;
}