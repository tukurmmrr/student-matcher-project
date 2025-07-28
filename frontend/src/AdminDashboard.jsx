import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_URL = 'https://tukur-student-matcher-project.onrender.com';

function MatchList({ title, description, matches, badgeClass }) {
  // ... (This component is correct from your last file upload)
}

function AdminDashboard() {
    const [matches, setMatches] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchMatches = async () => {
            const token = localStorage.getItem('accessToken');
            if (!token) { navigate('/login'); return; }
            try {
                const config = { headers: { Authorization: `Bearer ${token}` } };
                // --- FIX: CALL THE CORRECT ADMIN ENDPOINT ---
                const response = await axios.get(`${API_URL}/matches/admin`, config);
                setMatches(response.data);
            } catch (error) {
                console.error("Failed to fetch matches:", error);
                if (error.response && error.response.status === 401) { navigate('/login'); }
            }
            setLoading(false);
        };
        fetchMatches();
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
                description="Compares all student pairs."
                matches={matches}
                badgeClass="bg-primary"
            />
        </div>
    );
}
export default AdminDashboard;