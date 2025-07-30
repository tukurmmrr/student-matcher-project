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
                ) : ( <p>No matches found. Register more students to see results.</p> )}
            </div>
        </div>
    );
}

function AdminDashboard() {
    const [jaccardMatches, setJaccardMatches] = useState([]);
    const [diceMatches, setDiceMatches] = useState([]);
    const [allStudents, setAllStudents] = useState([]); // State for all users
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    const fetchAdminData = async () => {
        const token = localStorage.getItem('accessToken');
        if (!token) { navigate('/login'); return; }
        const config = { headers: { Authorization: `Bearer ${token}` } };

        try {
            const jaccardPromise = axios.get(`${API_URL}/admin/matches/jaccard`, config);
            const dicePromise = axios.get(`${API_URL}/admin/matches/dice`, config);
            const usersPromise = axios.get(`${API_URL}/admin/users`, config);

            const [jaccardRes, diceRes, usersRes] = await Promise.all([jaccardPromise, dicePromise, usersPromise]);

            setJaccardMatches(jaccardRes.data);
            setDiceMatches(diceRes.data);
            setAllStudents(usersRes.data);
        } catch (error) {
            console.error("Failed to fetch admin data:", error);
            if (error.response && (error.response.status === 401 || error.response.status === 403)) {
                navigate('/login');
            }
        }
        setLoading(false);
    };

    useEffect(() => {
        fetchAdminData();
    }, []);

    const handleDelete = async (userId, userName) => {
        if (window.confirm(`Are you sure you want to delete the user: ${userName}?`)) {
            const token = localStorage.getItem('accessToken');
            try {
                const config = { headers: { Authorization: `Bearer ${token}` } };
                await axios.delete(`${API_URL}/admin/users/${userId}`, config);
                fetchAdminData(); // Refresh all data after deletion
            } catch (error) {
                alert('Failed to delete user.');
            }
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('accessToken');
        navigate('/login');
    };

    if (loading) return <h4>Loading admin data...</h4>;

    return (
        <div>
            <div className="d-flex justify-content-between align-items-center mb-4">
                <h2 className="mb-0">Admin Dashboard</h2>
                <button onClick={handleLogout} className="btn btn-danger">Log Out</button>
            </div>

            <h3 className="mt-5">Algorithm Comparison</h3>
            <div className="row">
                <div className="col-lg-6"><MatchList title="Algorithm 1: Jaccard Similarity" matches={jaccardMatches} badgeClass="bg-primary"/></div>
                <div className="col-lg-6"><MatchList title="Algorithm 2: Dice Coefficient" matches={diceMatches} badgeClass="bg-success"/></div>
            </div>

            <hr className="my-5" />

            <h3 className="mt-5">User Management</h3>
            <div className="table-responsive">
                <table className="table table-striped">
                    <thead>
                        <tr><th>ID</th><th>Name</th><th>Email</th><th>Course</th><th>Interests</th><th>Actions</th></tr>
                    </thead>
                    <tbody>
                        {allStudents.map(user => (
                            <tr key={user.id}>
                                <td>{user.id}</td>
                                <td>{user.name}</td>
                                <td>{user.email}</td>
                                <td>{user.course ? user.course.name : 'N/A'}</td>
                                <td>{user.interests.map(i => i.name).join(', ')}</td>
                                <td>
                                    <button onClick={() => handleDelete(user.id, user.name)} className="btn btn-sm btn-outline-danger">Delete</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
export default AdminDashboard;