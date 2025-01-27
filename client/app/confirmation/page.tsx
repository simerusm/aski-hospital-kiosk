'use client';

import { ConfirmationPage } from './Confirmation';
import ProtectedRoute from '../components/ProtectedRoute';

export default function ModesPage() {
  return (
    <ProtectedRoute>
      <div>
        <ConfirmationPage/>
      </div>
    </ProtectedRoute>
  );
} 