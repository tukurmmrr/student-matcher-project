import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_URL = 'https://tukur-student-matcher-project.onrender.com'; // Your live Render URL

function UserDashboard() {
    const [matches, setMatches] = useState([]);
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const fetchUserData = async () => {
            const token = localStorage.getItem('accessToken');
            if (!token) {
                navigate('/login');
                return;
            }
            try {
                const config = { headers: { Authorization: `Bearer ${token}` } };
                // Fetch the logged-in user's data first
                const userRes = await axios.get(`${API_URL}/users/me`, config);
                setUser(userRes.data);

                // Then fetch the matches
                const matchRes = await axios.get(`${API_URL}/matches/cosine`, config);
                setMatches(matchRes.data);
            } catch (err) {
                setError('Could not fetch your data.');
            }
            setLoading(false);
        };
        fetchUserData();
    }, [navigate]);

    const handleLogout = () => {
        localStorage.removeItem('accessToken');
        navigate('/login');
    };

    if (loading) return <p>Loading your dashboard...</p>;
    if (error) return <p className="text-danger">{error}</p>;

    return (
        <div>
            <div className="d-flex justify-content-between align-items-center mb-4">
                 <h2>Welcome, {user?.name}!</h2>
                 <button onClick={handleLogout} className="btn btn-danger">Log Out</button>
            </div>

            <h4 className="mb-3">Your Top Matches (based on Cosine Similarity)</h4>

            {matches.length > 0 ? (
                <div className="list-group">
                    {matches.map((match, index) => (
                        <div key={index} className="list-group-item">
                            <div className="d-flex w-100 justify-content-between">
                                <h5 className="mb-1">{match.student.name}</h5>
                                <span className="badge bg-success rounded-pill" style={{fontSize: '1em'}}>{match.score.toFixed(2)}</span>
                            </div>
                            <p className="mb-1"><strong>Course:</strong> {match.student.course ? match.student.course.name : 'N/A'}</p>
                            <p className="mb-1"><strong>Shared Interests:</strong> {
                                user.interests.filter(i => match.student.interests.some(mi => mi.id === i.id)).map(i => i.name).join(', ') || 'None'
                            }</p>
                            <small className="text-muted">Contact: {match.student.email}</small>
                        </div>
                    ))}
                </div>
            ) : (
                <p>No matches found yet. Check back later!</p>
            )}
        </div>
    );
}
export default UserDashboard;