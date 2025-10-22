"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { RegisterForm } from '../components/AuthForms';

export default function RegisterPage() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const handleRegister = async (username: string, email: string, password: string) => {
    setLoading(true);
    setError(null);

    try {
      // TODO: Implement actual registration API call
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password }),
      });

      if (!response.ok) {
        throw new Error('Registration failed');
      }

      const data = await response.json();

      // Store JWT token
      localStorage.setItem('zion_auth_token', data.token);

      // Redirect to dashboard
      router.push('/dashboard-v2');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return <RegisterForm onRegister={handleRegister} loading={loading} error={error} />;
}