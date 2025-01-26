'use client';

import ModeSelection from './ModeSelection';
import ProtectedRoute from '../components/ProtectedRoute';

export default function ModesPage() {
  return (
    <ProtectedRoute>
      <div>
        <ModeSelection />
      </div>
    </ProtectedRoute>
  );
} 