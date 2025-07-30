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
                                    <strong>{match.student1.name}</strong> ↔ <strong>{match.student2.name}</strong>
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
    const [jaccardMatches, setJaccardMatches] = useState([]);
    const [diceMatches, setDiceMatches] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem('accessToken');
        if (!token) { navigate('/login'); return; }
        const config = { headers: { Authorization: `Bearer ${token}` } };

        const fetchAdminData = async () => {
            setLoading(true);
            try {
                // Fetch both sets of algorithm results in parallel
                const jaccardPromise = axios.get(`${API_URL}/admin/matches/jaccard`, config);
                const dicePromise = axios.get(`${API_URL}/admin/matches/dice`, config);

                const [jaccardRes, diceRes] = await Promise.all([jaccardPromise, dicePromise]);

                setJaccardMatches(jaccardRes.data);
                setDiceMatches(diceRes.data);

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
                <h2 className="mb-0">Admin Dashboard: Algorithm Comparison</h2>
                <button onClick={handleLogout} className="btn btn-danger">Log Out</button>
            </div>
            <div className="row">
                <div className="col-lg-6">
                    <MatchList
                        title="Algorithm 1: Jaccard Similarity"
                        description="Scores based on Intersection over Union."
                        matches={jaccardMatches}
                        badgeClass="bg-primary"
                    />
                </div>
                <div className="col-lg-6">
                    <MatchList
                        title="Algorithm 2: Dice Coefficient"
                        description="Scores based on 2 * Intersection / (Size A + Size B)."
                        matches={diceMatches}
                        badgeClass="bg-success"
                    />
                </div>
            </div>
        </div>
    );
}

export default AdminDashboard;