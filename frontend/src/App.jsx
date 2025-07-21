import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';

// This code assumes your components are in the SAME folder as App.jsx
import LoginPage from './LoginPage.js';
import RegisterPage from './RegisterPage.js';
import Dashboard from './Dashboard.js';

import './App.css'

function App() {
  return (
    <Router>
        <div className="container mt-4">
            <header className="text-center mb-5">
                <h1>🎓 Student Buddy System</h1>
            </header>
            <main>
                <Routes>
                    <Route path="/" element={<Navigate to="/login" />} />
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/register" element={<RegisterPage />} />
                    <Route path="/dashboard" element={<Dashboard />} />
                </Routes>
            </main>
        </div>
    </Router>
  );
}

export default App;