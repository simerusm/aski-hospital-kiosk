'use client';

import { useState } from 'react';
import { patientService } from '../services/patients/patientsApi';
import { useRouter } from 'next/navigation';

export default function PatientAuth() {
  const router = useRouter();
  const [ssn, setSsn] = useState('');
  const [phone, setPhone] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await patientService.authenticate(ssn, phone);
      if (response.status === 200) {
        setMessage('Authentication successful!');
        router.push('/modes'); // Redirect to the modes page after authentication
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

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl text-gray-700 font-bold mb-6">Patient Authentication</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-gray-700 mb-2">SSN:</label>
          <input
            type="text"
            value={ssn}
            onChange={(e) => setSsn(e.target.value)}
            className="w-full text-gray-700 p-2 border rounded"
            required
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 mb-2">Phone:</label>
          <input
            type="tel"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
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
  );
}