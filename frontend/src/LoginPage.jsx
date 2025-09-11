import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';

const API_BASE_URL = 'https://tukur-student-matcher-project.onrender.com';

function LoginPage() {
    const [credentials, setCredentials] = useState({ username: '', password: '' });
    const [errorMessage, setErrorMessage] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const navigate = useNavigate();

    const updateField = (e) => {
        const { name, value } = e.target;
        setCredentials(prev => ({ ...prev, [name]: value }));
    };

    const submitLogin = async (e) => {
        e.preventDefault();
        setErrorMessage('');
        setIsSubmitting(true);

        try {
            // Format data for form submission
            const loginParams = new URLSearchParams();
            loginParams.append('username', credentials.username);
            loginParams.append('password', credentials.password);

            const response = await axios.post(`${API_BASE_URL}/token`, loginParams);

            // Store the auth token and redirect
            localStorage.setItem('accessToken', response.data.access_token);
            navigate('/dashboard');
        } catch (error) {
            console.warn('Login attempt failed:', error);
            const message = error.response?.data?.detail || 'Login failed. Please check your credentials.';
            setErrorMessage(message);
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="card shadow-sm">
            <div className="card-body">
                <h3 className="card-title text-center mb-4">Welcome Back</h3>
                <form onSubmit={submitLogin}>
                    {errorMessage && (
                        <div className="alert alert-danger" role="alert">
                            {errorMessage}
                        </div>
                    )}

                    <div className="mb-3">
                        <label className="form-label">Email Address</label>
                        <input
                            type="email"
                            name="username"
                            className="form-control"
                            value={credentials.username}
                            onChange={updateField}
                            required
                            disabled={isSubmitting}
                        />
                    </div>

                    <div className="mb-3">
                        <label className="form-label">Password</label>
                        <input
                            type="password"
                            name="password"
                            className="form-control"
                            value={credentials.password}
                            onChange={updateField}
                            required
                            disabled={isSubmitting}
                        />
                    </div>

                    <button
                        type="submit"
                        className="btn btn-primary w-100"
                        disabled={isSubmitting}
                    >
                        {isSubmitting ? 'Signing In...' : 'Log In'}
                    </button>

                    <p className="text-center mt-3">
                        New here? <Link to="/register">Create an account</Link>
                    </p>
                </form>
            </div>
        </div>
    );
}

export default LoginPage;