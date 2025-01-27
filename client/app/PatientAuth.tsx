'use client';

import { useState, useEffect } from 'react';
import { patientService } from './services/patients/patientsApi';
import { useRouter } from 'next/navigation';
import { useAuth } from './context/AuthContext';
import PageWrapper from './components/PageWrapper';

export default function PatientAuth() {
  const router = useRouter();
  const { login, isAuthenticated, isLoading } = useAuth();
  const [mounted, setMounted] = useState(false);
  const [formState, setFormState] = useState({
    ssn: '',
    phone: '',
  });
  const [message, setMessage] = useState('');

  useEffect(() => {
    setMounted(true);
    // Restore form state from sessionStorage if it exists
    const savedState = sessionStorage.getItem('authFormState');
    if (savedState) {
      setFormState(JSON.parse(savedState));
    }
  }, []);

  // Redirect if already authenticated
  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      router.push('/modes');
    }
  }, [isLoading, isAuthenticated, router]);

  // Save form state to sessionStorage when it changes
  useEffect(() => {
    if (mounted) {
      sessionStorage.setItem('authFormState', JSON.stringify(formState));
    }
  }, [formState, mounted]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormState(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await patientService.authenticate(formState.ssn, formState.phone);
      if (response.status === 200) {
        const { token, user } = response.data.response;
        login(token, user);
        setMessage('Authentication successful!');
        // Clear form state from sessionStorage after successful login
        sessionStorage.removeItem('authFormState');
        router.push('/modes');
      }
    } catch (error: unknown) {
      if (typeof error === 'object' && error !== null && 'response' in error) {
        const errorResponse = error as { response?: { data?: { message?: string } } };
        setMessage(errorResponse.response?.data?.message || 'Authentication failed');
      } else if (error instanceof Error) {
        setMessage(error.message);
      } else {
        setMessage('Authentication failed');
      }
    }
  };

  // Don't render anything while loading or if authenticated
  if (!mounted || isLoading || isAuthenticated) {
    return null;
  }

  return (
    <PageWrapper>
      <div className="max-w-md mx-auto mt-25 p-9 bg-white rounded-lg shadow-lg">
        <h2 className="text-2xl text-gray-700 font-bold mb-6">Patient Authentication</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700 mb-2">SSN:</label>
            <input
              type="text"
              name="ssn"
              value={formState.ssn}
              onChange={handleInputChange}
              className="w-full text-gray-700 p-2 border rounded"
              required
            />
          </div>
          <div className="mb-4">
            <label className="block text-gray-700 mb-2">Phone:</label>
            <input
              type="tel"
              name="phone"
              value={formState.phone}
              onChange={handleInputChange}
              className="w-full text-gray-700 p-2 border rounded"
              required
            />
          </div>
          <button
            type="submit"
            className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
          >
            Authenticate
          </button>
        </form>
        {message && (
          <p className="mt-4 text-gray-700 text-center text-sm">
            {message}
          </p>
        )}
      </div>
    </PageWrapper>
  );
}