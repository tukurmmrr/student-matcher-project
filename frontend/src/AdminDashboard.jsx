import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_URL = 'https://tukur-student-matcher-project.onrender.com/'; // Use your live Render URL

function MatchList({ title, description, matches, badgeClass }) {
  // ... (MatchList component code from before, no changes needed here) ...
}

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
                    {/* ... (Jaccard MatchList component from before) ... */}
                </div>
                <div className="col-lg-6">
                    {/* ... (Cosine MatchList component from before) ... */}
                </div>
            </div>
        </div>
    );
}

export default AdminDashboard;