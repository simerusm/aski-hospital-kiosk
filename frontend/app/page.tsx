"use client"
import { useState } from 'react';
import PatientAuth from './components/PatientAuth';
import ModeSelection from './components/ModeSelection';

export default function Home() {
  const [authenticated, setAuthenticated] = useState(false);

  const handleAuthentication = () => {
    setAuthenticated(true);
  };

  return (
    <main className="min-h-screen p-8">
      {!authenticated ? (
        <PatientAuth onAuthenticate={handleAuthentication} />
      ) : (
        <ModeSelection />
      )}
    </main>
  );
}