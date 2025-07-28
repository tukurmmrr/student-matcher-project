import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_URL = 'https://tukur-student-matcher-project.onrender.com';

function UserDashboard() {
    const [matches, setMatches] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem('accessToken');
        if (!token) { navigate('/login'); return; }
        try {
            const config = { headers: { Authorization: `Bearer ${token}` } };
            // Fetch matches from the dedicated user endpoint
            axios.get(`${API_URL}/matches/user`, config).then(response => {
                setMatches(response.data);
                setLoading(false);
            });
        } catch (err) {
            console.error("Could not fetch matches:", err);
            setLoading(false);
        }
    }, [navigate]);

    const handleLogout = () => {
        localStorage.removeItem('accessToken');
        navigate('/login');
    };

    if (loading) return <p>Loading your matches...</p>;

    return (
        <div>
            <div className="d-flex justify-content-between align-items-center mb-4">
                 <h2>Your Best Match Is:</h2>
                 <button onClick={handleLogout} className="btn btn-danger">Log Out</button>
            </div>
            {matches.length > 0 ? (
                <div className="card">
                    <div className="card-body">
                        <h5 className="card-title">{matches[0].student.name}</h5>
                        <h6 className="card-subtitle mb-2 text-muted">{matches[0].student.course.name}</h6>
                        <p className="card-text">
                            <strong>Contact:</strong> <a href={`mailto:${matches[0].student.email}`}>{matches[0].student.email}</a>
                        </p>
                    </div>
                </div>
            ) : (
                <p>No matches found yet. You will be matched when new students register!</p>
            )}
        </div>
    );
}
export default UserDashboard;