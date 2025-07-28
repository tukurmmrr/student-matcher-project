import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_URL = 'https://tukur-student-matcher-project.onrender.com'; // Your live Render URL

function UserDashboard() {
    const [matches, setMatches] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const fetchMatches = async () => {
            const token = localStorage.getItem('accessToken');
            if (!token) {
                navigate('/login');
                return;
            }
            try {
                const config = { headers: { Authorization: `Bearer ${token}` } };
                const response = await axios.get(`${API_URL}/matches/cosine`, config);
                setMatches(response.data);
            } catch (err) {
                setError('Could not fetch your matches.');
            }
            setLoading(false);
        };
        fetchMatches();
    }, [navigate]);

    const handleLogout = () => {
        localStorage.removeItem('accessToken');
        navigate('/login');
    };

    if (loading) return <p>Loading your matches...</p>;
    if (error) return <p className="text-danger">{error}</p>;

    return (
        <div>
            <div className="d-flex justify-content-between align-items-center mb-4">
                 <h2>Your Top Matches</h2>
                 <button onClick={handleLogout} className="btn btn-danger">Log Out</button>
            </div>
            {matches.length > 0 ? (
                <ul className="list-group">
                    {matches.map((match, index) => (
                        <li key={index} className="list-group-item d-flex justify-content-between align-items-center">
                           <div>
                             <h5>{match.student.name}</h5>
                             {/* This line is now safe because the backend guarantees the course object exists */}
                             <p className="mb-0 text-muted">Course: {match.student.course.name}</p>
                           </div>
                           <span className="badge bg-success rounded-pill">{match.score.toFixed(2)}</span>
                        </li>
                    ))}
                </ul>
            ) : (
                <p>No matches found yet. Register more students to see results!</p>
            )}
        </div>
    );
}
export default UserDashboard;