import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_URL = 'https://tukur-student-matcher-project.onrender.com';

function MatchList({ title, description, matches, badgeClass }) {
  return (
    <div className="card shadow-sm mb-4">
        <div className="card-body">
            <h3 className="card-title">{title}</h3>
            <p className="card-text text-muted">{description}</p>
            {matches.length > 0 ? (
                <ul className="list-group">
                {matches.map((match, index) => (
                    <li key={index} className="list-group-item d-flex justify-content-between align-items-center">
                        <span>
                            <strong>{match.student1.name}</strong> ({match.student1.course}) ↔ <strong>{match.student2.name}</strong> ({match.student2.course})
                        </span>
                        <span className={`badge ${badgeClass} rounded-pill`}>{match.score}</span>
                    </li>
                ))}
                </ul>
            ) : (
                <p>No matches found. Register more students to see results.</p>
            )}
        </div>
    </div>
  );
}

function AdminDashboard() {
    const [matches, setMatches] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem('accessToken');
        if (!token) {
            navigate('/login');
            return;
        }
        const config = { headers: { Authorization: `Bearer ${token}` } };

        const fetchAdminData = async () => {
            setLoading(true);
            try {
                // Fetch all matches for the comparison view
                const response = await axios.get(`${API_URL}/matches/admin`, config);
                setMatches(response.data);

            } catch (error) {
                console.error("Failed to fetch admin data:", error);
                if (error.response && (error.response.status === 401 || error.response.status === 403)) {
                    navigate('/login');
                }
            }
            setLoading(false);
        };
        fetchAdminData();
    }, [navigate]);

    const handleLogout = () => {
        localStorage.removeItem('accessToken');
        navigate('/login');
    };

    if (loading) return <h4>Loading admin data...</h4>;

    return (
        <div>
            <div className="d-flex justify-content-between align-items-center mb-4">
                <h2 className="mb-0">Admin Dashboard: All Matches</h2>
                <button onClick={handleLogout} className="btn btn-danger">Log Out</button>
            </div>
            <MatchList
                title="Jaccard Similarity Comparison"
                description="Compares all student pairs with their match scores."
                matches={matches}
                badgeClass="bg-primary"
            />
        </div>
    );
}
export default AdminDashboard;