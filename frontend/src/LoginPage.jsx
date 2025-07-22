import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';

const API_URL = 'https://tukur-student-matcher-project.onrender.com'; // Use your live Render URL

function LoginPage() {
    const [formData, setFormData] = useState({ username: '', password: '' });
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try {
            const params = new URLSearchParams();
            params.append('username', formData.username);
            params.append('password', formData.password);

            const response = await axios.post(`${API_URL}/token`, params);
            localStorage.setItem('accessToken', response.data.access_token);
            window.location.href = '/dashboard'; // Force a full page reload to update state
        } catch (err) {
            setError(err.response?.data?.detail || 'Login failed.');
        }
    };

    return (
        <div className="card shadow-sm">
            <div className="card-body">
                <h3 className="card-title text-center mb-4">Log In</h3>
                <form onSubmit={handleSubmit}>
                    {error && <div className="alert alert-danger">{error}</div>}
                    <div className="mb-3">
                        <label className="form-label">Email (as username)</label>
                        <input type="email" name="username" className="form-control" onChange={handleChange} required />
                    </div>
                    <div className="mb-3">
                        <label className="form-label">Password</label>
                        <input type="password" name="password" className="form-control" onChange={handleChange} required />
                    </div>
                    <button type="submit" className="btn btn-primary w-100">Log In</button>
                    <p className="text-center mt-3">
                        Don't have an account? <Link to="/register">Register here</Link>
                    </p>
                </form>
            </div>
        </div>
    );
}
export default LoginPage;