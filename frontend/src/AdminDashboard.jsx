import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_URL = 'https://tukur-student-matcher-project.onrender.com'; // Use your live Render URL

// --- THIS COMPONENT WAS MISSING ---
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
                        {match.student1.name} ↔ {match.student2.name}
                        <span className={`badge ${badgeClass} rounded-pill`}>{match.score}</span>
                    </li>
                ))}
                </ul>
            ) : (
                <p>No matches found.</p>
            )}
        </div>
    </div>
  );
}
// ------------------------------------

function AdminDashboard() {
    const [jaccardMatches, setJaccardMatches] = useState([]);
    const [cosineMatches, setCosineMatches] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchMatches = async () => {
            setLoading(true);
            try {
                const token = localStorage.getItem('accessToken');
                if (!token) {
                    navigate('/login');
                    return;
                }
                const config = { headers: { Authorization: `Bearer ${token}` } };

                const jaccardRes = await axios.get(`${API_URL}/matches/jaccard`, config);
                const cosineRes = await axios.get(`${API_URL}/matches/cosine`, config);
                setJaccardMatches(jaccardRes.data);
                setCosineMatches(cosineRes.data);
            } catch (error) {
                console.error("Failed to fetch matches:", error);
                if (error.response && error.response.status === 401) {
                    navigate('/login');
                }
            }
            setLoading(false);
        };
        fetchMatches();
    }, [navigate]);

    const handleLogout = () => {
        localStorage.removeItem('accessToken');
        navigate('/login');
    };

    if (loading) {
        return <div className="text-center"><h4>Loading admin data...</h4></div>;
    }

    return (
        <div>
            <div className="d-flex justify-content-between align-items-center mb-4">
                <h2 className="mb-0">Admin Dashboard: Algorithm Comparison</h2>
                <button onClick={handleLogout} className="btn btn-danger">Log Out</button>
            </div>
            <a href="/register" className="btn btn-secondary mb-4">Register Another Student</a>
            <div className="row">
                <div className="col-lg-6">
                    <MatchList
                        title="Jaccard Similarity"
                        description="Measures simple overlap."
                        matches={jaccardMatches}
                        badgeClass="bg-primary"
                      />
                </div>
                <div className="col-lg-6">
                     <MatchList
                        title="Cosine Similarity"
                        description="Weighs rare interests more heavily."
                        matches={cosineMatches}
                        badgeClass="bg-success"
                      />
                </div>
            </div>
        </div>
    );
}

export default AdminDashboard;