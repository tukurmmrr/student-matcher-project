// frontend/src/App.js

import React, { useState } from 'react';
import RegistrationForm from './components/RegistrationForm';
import Dashboard from './components/Dashboard';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [isRegistered, setIsRegistered] = useState(false);

  const handleRegistrationSuccess = () => {
    setIsRegistered(true);
  };

  return (
    <div className="container mt-4">
      <header className="text-center mb-5">
        <h1>🎓 Student Buddy System</h1>
        <p className="lead">Find your study partners and friends!</p>
      </header>

      {!isRegistered ? (
        <RegistrationForm onSuccess={handleRegistrationSuccess} />
      ) : (
        <Dashboard />
      )}
    </div>
  );
}

export default App;