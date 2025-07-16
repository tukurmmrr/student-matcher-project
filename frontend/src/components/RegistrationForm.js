// frontend/src/components/RegistrationForm.js

import React, { useState } from 'react';
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

function RegistrationForm({ onSuccess }) {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    course: '',
    interests: '',
    bio: '',
    profile_picture_url: ''
  });

  // --- NEW STATE TO MANAGE THE NEWLY CREATED STUDENT ---
  const [newStudent, setNewStudent] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setNewStudent(null); // Clear previous new student

    if (!formData.name || !formData.email || !formData.course || !formData.interests) {
      setError('Required fields are missing.');
      return;
    }

    try {
      const response = await axios.post(`${API_URL}/students/`, formData);
      setSuccess(`Success! Student '${response.data.name}' was created.`);
      setNewStudent(response.data); // Save the new student's data
      setFormData({ name: '', email: '', course: '', interests: '', bio: '', profile_picture_url: '' }); // Clear the form
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred during registration.');
    }
  };

  // --- NEW FUNCTION TO HANDLE DELETING THE PROFILE ---
  const handleDelete = async () => {
    if (!newStudent) return;
    setError('');

    try {
      await axios.delete(`${API_URL}/students/${newStudent.id}`);
      setSuccess(`Profile for '${newStudent.name}' was successfully deleted.`);
      setNewStudent(null); // Clear the deleted student's data
    } catch (err) {
      setError(err.response?.data?.detail || 'Could not delete the profile.');
    }
  };


  return (
    <div className="card shadow-sm">
      <div className="card-body">
        {/* --- NEW LOGIC TO SHOW A DIFFERENT VIEW AFTER SUCCESS --- */}
        {newStudent ? (
          <div className="text-center">
            {error && <div className="alert alert-danger">{error}</div>}
            {success && <div className="alert alert-success">{success}</div>}
            <h4 className="mb-3">Manage New Profile</h4>
            <p>Student '<strong>{newStudent.name}</strong>' has been created.</p>
            <button onClick={handleDelete} className="btn btn-danger me-2">Delete This Profile</button>
            <button onClick={onSuccess} className="btn btn-primary">Go to Dashboard</button>
          </div>
        ) : (
          <div>
            <h3 className="card-title text-center mb-4">Register Your Interests</h3>
            <form onSubmit={handleSubmit}>
              {error && <div className="alert alert-danger">{error}</div>}
              {success && <div className="alert alert-success">{success}</div>}

              <div className="mb-3">
                <label className="form-label">Full Name</label>
                <input type="text" name="name" className="form-control" value={formData.name} onChange={handleChange} required />
              </div>
              <div className="mb-3">
                <label className="form-label">Email</label>
                <input type="email" name="email" className="form-control" value={formData.email} onChange={handleChange} required />
              </div>
              <div className="mb-3">
                <label className="form-label">Course of Study</label>
                <input type="text" name="course" className="form-control" value={formData.course} onChange={handleChange} required />
              </div>
              <div className="mb-3">
                <label className="form-label">Interests (comma-separated)</label>
                <input type="text" name="interests" className="form-control" value={formData.interests} onChange={handleChange} required />
              </div>

              <div className="mb-3">
                <label className="form-label">Short Bio</label>
                <textarea name="bio" className="form-control" rows="3" placeholder="Tell us a little about yourself..." value={formData.bio} onChange={handleChange}></textarea>
              </div>
              <div className="mb-3">
                <label className="form-label">Profile Picture URL</label>
                <input type="text" name="profile_picture_url" className="form-control" placeholder="https://example.com/your-image.jpg" value={formData.profile_picture_url} onChange={handleChange} />
              </div>

              <button type="submit" className="btn btn-primary w-100">Register</button>
            </form>
          </div>
        )}
      </div>
    </div>
  );
}

export default RegistrationForm;