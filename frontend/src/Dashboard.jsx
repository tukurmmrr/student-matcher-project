import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import AdminDashboard from './AdminDashboard.jsx';
import UserDashboard from './UserDashboard.jsx';

const API_URL = 'https://tukur-student-matcher-project.onrender.com/'; // Use your live Render URL

function Dashboard() {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchUser = async () => {
            const token = localStorage.getItem('accessToken');
            if (!token) {
                navigate('/login');
                return;
            }

            try {
                const config = { headers: { Authorization: `Bearer ${token}` } };
                const response = await axios.get(`${API_URL}/users/me`, config);
                setUser(response.data);
            } catch (error) {
                console.error("Failed to fetch user:", error);
                localStorage.removeItem('accessToken');
                navigate('/login');
            }
            setLoading(false);
        };
        fetchUser();
    }, [navigate]);

    if (loading) {
        return <div className="text-center"><h4>Loading dashboard...</h4></div>;
    }

    // This is the logic that shows the correct dashboard
    return user && user.is_admin ? <AdminDashboard /> : <UserDashboard />;
}

export default Dashboard;