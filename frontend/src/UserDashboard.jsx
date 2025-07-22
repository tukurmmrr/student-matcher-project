import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_URL = 'https://tukur-student-matcher-project.onrender.com/'; // Testing locally

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
                // We'll just use the cosine similarity for the user's view
                const response = await axios.get(`${API_URL}/matches/cosine`, config);
                setMatches(response.data);
            } catch (err) {
                setError('Could not fetch your matches.');
            }
            setLoading(false);
        };
        fetchMatches();
    }, [navigate]);

    // ... (Logout handler) ...

    if (loading) return <p>Loading your matches...</p>;
    if (error) return <p className="text-danger">{error}</p>;

    return (
        <div>
            <h2>Your Top Matches</h2>
            {matches.length > 0 ? (
                <ul className="list-group">
                    {matches.map((match, index) => (
                        <li key={index} className="list-group-item">
                            <h5>{match.student.name}</h5>
                            <p>Course: {match.student.course ? match.student.course.name : 'N/A'}</p>
                            <p>Bio: {match.student.bio || 'No bio provided.'}</p>
                            <span className="badge bg-success">{match.score.toFixed(2)}</span>
                        </li>
                    ))}
                </ul>
            ) : (
                <p>No matches found yet. Check back later!</p>
            )}
            {/* ... (Logout button) ... */}
        </div>
    );
}
export default UserDashboard;