'use client';

import { useRouter } from 'next/navigation';
import { slotsService } from '../services/slots/slotsApi';

export default function ModeSelection() {
  const router = useRouter();

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

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl text-gray-700 font-bold mb-6">Select Your Mode</h2>
      <div className="mb-4">
        <button
          onClick={handleWalkIn}
          className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600 mb-2"
        >
          Walk-In Queue
        </button>
        <button
          onClick={handleAppointment}
          className="w-full bg-green-500 text-white py-2 rounded hover:bg-green-600"
        >
          Book an Appointment
        </button>
      </div>
    </div>
  );
} 