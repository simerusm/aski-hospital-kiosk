'use client';

import { useRouter } from 'next/navigation';
import { slotsService } from '../services/slots/slotsApi';
import { useAuth } from '../context/AuthContext';

export default function ModeSelection() {
  const router = useRouter();
  const { logout, user } = useAuth();

  const handleWalkIn = async () => {
    // Redirect to the queue join endpoint
    await fetch('/api/queue/join', {
      method: 'POST',
      // Include any necessary data here
    });
    router.push('/queue'); // Redirect to a queue status page or similar
  };

  const handleAppointment = async () => {
    // Fetch available slots
    try {
      const response = await slotsService.getSlots();
      if (response.status === 200) {
        console.log(response.data); // Handle the response data as needed
        router.push('/slots'); // Redirect to a slots page
      }
    } catch (error) {
      console.error(error);
    }
  };

  const handleLogout = () => {
    logout();
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-lg">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl text-gray-700 font-bold">Select Your Mode</h2>
        <button
          onClick={handleLogout}
          className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 text-sm"
        >
          Logout
        </button>
      </div>
      {user && (
        <p className="text-gray-600 mb-4">
          Welcome, {user.name}
        </p>
      )}
      <div className="space-y-4">
        <button
          onClick={handleWalkIn}
          className="w-full bg-blue-500 text-white py-3 rounded hover:bg-blue-600 transition-colors"
        >
          Walk-In Queue
        </button>
        <button
          onClick={handleAppointment}
          className="w-full bg-green-500 text-white py-3 rounded hover:bg-green-600 transition-colors"
        >
          Book an Appointment
        </button>
      </div>
    </div>
  );
} 