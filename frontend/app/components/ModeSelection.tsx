'use client';

import { useRouter } from 'next/navigation';
import { slotService } from '../services/api';

export default function ModeSelection() {
  const router = useRouter();

  const handleWalkIn = () => {
    // Redirect to the queue join endpoint
    router.push('/api/queue/join');
  };

  const handleAppointment = async () => {
    // Mock API call
    try {
        const response = await slotService.getSlots();
        if (response.status === 200) {
            console.log(response.data.response)
        } 
    } catch(error) {
        console.log(error)
    }
    
    // Redirect to the available slots endpoint
    router.push('/api/slots/available');
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