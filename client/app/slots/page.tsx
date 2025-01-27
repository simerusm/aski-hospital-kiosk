'use client';

import AppointmentCalendar from './AppointmentCalendar';
import ProtectedRoute from '../components/ProtectedRoute';

export default function AvailableSlots() {
  return (
    <ProtectedRoute>
      <div>
        <AppointmentCalendar />
      </div>
    </ProtectedRoute>
  );
} 