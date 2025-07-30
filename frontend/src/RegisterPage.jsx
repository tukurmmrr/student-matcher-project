import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';

const API_URL = 'https://tukur-student-matcher-project.onrender.com'; // Your live Render URL

function RegisterPage() {
    const [step, setStep] = useState(1);
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: '',
        course_id: '',
    });
    const [interests, setInterests] = useState([]);
    const [courses, setCourses] = useState([]);
    const [selectedInterests, setSelectedInterests] = useState(new Set());
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const fetchData = async () => {
            try {
                const coursesRes = await axios.get(`${API_URL}/courses`);
                const interestsRes = await axios.get(`${API_URL}/interests`);
                setCourses(coursesRes.data);
                setInterests(interestsRes.data);
            } catch (err) {
                setError('Could not load registration data from the server.');
            }
        };
        fetchData();
    }, []);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleInterestChange = (interestId) => {
        const newSelectedInterests = new Set(selectedInterests);
        if (newSelectedInterests.has(interestId)) {
            newSelectedInterests.delete(interestId);
        } else {
            newSelectedInterests.add(interestId);
        }
        setSelectedInterests(newSelectedInterests);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');

        if (!formData.course_id || selectedInterests.size === 0) {
            setError('Please select a course and at least one interest.');
            return;
        }

        const registrationData = {
            ...formData,
            course_id: parseInt(formData.course_id),
            interest_ids: Array.from(selectedInterests),
        };

        try {
            await axios.post(`${API_URL}/register`, registrationData);
            setSuccess('Registration successful! Please log in.');
            setTimeout(() => navigate('/login'), 2000);
        } catch (err) {
            setError(err.response?.data?.detail || 'Registration failed.');
        }
    };

    return (
        <div className="card shadow-sm">
            <div className="card-body">
                <h3 className="card-title text-center mb-4">Create Your Account</h3>
                {error && <div className="alert alert-danger">{error}</div>}
                {success && <div className="alert alert-success">{success}</div>}

                {step === 1 && (
                    <form onSubmit={(e) => { e.preventDefault(); setStep(2); }}>
                        <div className="mb-3">
                            <label className="form-label">Full Name</label>
                            <input type="text" name="name" className="form-control" value={formData.name} onChange={handleChange} required />
                        </div>
                        <div className="mb-3">
                            <label className="form-label">Email</label>
                            <input type="email" name="email" className="form-control" value={formData.email} onChange={handleChange} required />
                        </div>
                        <div className="mb-3">
                            <label className="form-label">Password</label>
                            <input type="password" name="password" className="form-control" value={formData.password} onChange={handleChange} required />
                        </div>
                        <button type="submit" className="btn btn-primary w-100">Next: Select Course & Interests</button>
                    </form>
                )}

                {step === 2 && (
                    <form onSubmit={handleSubmit}>
                         <div className="mb-3">
                            <label className="form-label">Course of Study</label>
                            <select name="course_id" className="form-select" value={formData.course_id} onChange={handleChange} required>
                                <option value="" disabled>Select your course</option>
                                {courses.map(course => (
                                    <option key={course.id} value={course.id}>{course.name}</option>
                                ))}
                            </select>
                        </div>
                        <div className="mb-3">
                            <label className="form-label">Interests</label>
                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                                {interests.map(interest => (
                                    <div key={interest.id} className="form-check">
                                        <input className="form-check-input" type="checkbox" id={`interest-${interest.id}`} onChange={() => handleInterestChange(interest.id)} checked={selectedInterests.has(interest.id)}/>
                                        <label className="form-check-label" htmlFor={`interest-${interest.id}`}>{interest.name}</label>
                                    </div>
                                ))}
                            </div>
                        </div>
                        <div className="d-flex justify-content-between">
                            <button type="button" className="btn btn-secondary" onClick={() => setStep(1)}>Back</button>
                            <button type="submit" className="btn btn-success">Complete Registration</button>
                        </div>
                    </form>
                )}
                 <p className="text-center mt-3">Already have an account? <Link to="/login">Login</Link></p>
            </div>
        </div>
    );
}

export default RegisterPage;