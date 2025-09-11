import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_BASE_URL = 'https://tukur-student-matcher-project.onrender.com';

function UserDashboard() {
    const [bestMatch, setBestMatch] = useState(null);
    const [isLoadingMatch, setIsLoadingMatch] = useState(true);
    const [fetchError, setFetchError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const loadUserMatches = async () => {
            const authToken = localStorage.getItem('accessToken');

            // Redirect if not authenticated
            if (!authToken) {
                navigate('/login');
                return;
            }

            try {
                const requestConfig = {
                    headers: { Authorization: `Bearer ${authToken}` }
                };

                const response = await axios.get(`${API_BASE_URL}/matches/user`, requestConfig);

                // Take the first (best) match if any exist
                if (response.data && response.data.length > 0) {
                    setBestMatch(response.data[0]);
                }
            } catch (error) {
                console.error("Error fetching matches:", error);
                setFetchError('Unable to load your matches right now.');
            } finally {
                setIsLoadingMatch(false);
            }
        };

        loadUserMatches();
    }, [navigate]);

    const signOut = () => {
        localStorage.removeItem('accessToken');
        navigate('/login');
    };

    if (isLoadingMatch) {
        return (
            <div className="text-center">
                <div className="spinner-border" role="status">
                    <span className="visually-hidden">Finding your best match...</span>
                </div>
                <p className="mt-2">Finding your best match...</p>
            </div>
        );
    }

    return (
        <div>
            <div className="d-flex justify-content-between align-items-center mb-4">
                <h2>Your Student Dashboard</h2>
                <button onClick={signOut} className="btn btn-outline-danger">
                    Sign Out
                </button>
            </div>

            {fetchError && (
                <div className="alert alert-warning" role="alert">
                    {fetchError}
                </div>
            )}

            {bestMatch ? (
                <div className="card text-center shadow-sm">
                    <div className="card-header bg-primary text-white">
                        <h5 className="mb-0">🎯 Your Best Match</h5>
                    </div>
                    <div className="card-body">
                        <h4 className="card-title text-primary">
                            {bestMatch.student.name}
                        </h4>
                        <p className="card-text">
                            Currently studying <strong>{bestMatch.student.course.name}</strong>
                        </p>
                        <a
                            href={`mailto:${bestMatch.student.email}`}
                            className="btn btn-primary"
                        >
                            📧 Contact {bestMatch.student.name}
                        </a>
                    </div>
                </div>
            ) : (
                <div className="alert alert-info text-center" role="alert">
                    <h5>No matches yet!</h5>
                    <p className="mb-0">
                        We'll find you a great study buddy as soon as more students join.
                        Check back soon! 🚀
                    </p>
                </div>
            )}
        </div>
    );
}

export default UserDashboard;