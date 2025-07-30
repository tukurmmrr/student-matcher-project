import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_URL = 'https://tukur-student-matcher-project.onrender.com'; // Your Render URL

function UserDashboard() {
    const [match, setMatch] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem('accessToken');
        if (!token) { navigate('/login'); return; }
        const config = { headers: { Authorization: `Bearer ${token}` } };

        axios.get(`${API_URL}/matches/user`, config)
            .then(response => {
                if (response.data && response.data.length > 0) {
                    setMatch(response.data[0]); // Only store the top match
                }
                setLoading(false);
            })
            .catch(err => {
                console.error("Could not fetch matches:", err);
                setLoading(false);
            });
    }, [navigate]);

    const handleLogout = () => {
        localStorage.removeItem('accessToken');
        navigate('/login');
    };

    if (loading) return <p>Finding your best match...</p>;

    return (
        <div>
            <div className="d-flex justify-content-between align-items-center mb-4">
                 <h2>Your Dashboard</h2>
                 <button onClick={handleLogout} className="btn btn-danger">Log Out</button>
            </div>
            {match ? (
                <div className="card text-center">
                    <div className="card-header">Your Best Match Is:</div>
                    <div className="card-body">
                        <h5 className="card-title">{match.student.name}</h5>
                        <p className="card-text">
                            A student in the **{match.student.course.name}** program.
                        </p>
                        <a href={`mailto:${match.student.email}`} className="btn btn-primary">Contact {match.student.name}</a>
                    </div>
                </div>
            ) : (
                <p>No matches found yet. You will be matched when new students register!</p>
            )}
        </div>
    );
}

export default UserDashboard;