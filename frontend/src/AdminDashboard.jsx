import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';

const API_URL = 'https://tukur-student-matcher-project.onrender.com'

function AdminDashboard() {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    const fetchUsers = async () => {
        const token = localStorage.getItem('accessToken');
        if (!token) { navigate('/login'); return; }
        try {
            const config = { headers: { Authorization: `Bearer ${token}` } };
            const response = await axios.get(`${API_URL}/admin/users`, config);
            setUsers(response.data);
        } catch (error) {
            console.error("Failed to fetch users:", error);
            if (error.response && error.response.status === 401) { navigate('/login'); }
        }
        setLoading(false);
    };

    useEffect(() => {
        fetchUsers();
    }, []);

    const handleDelete = async (userId) => {
        if (window.confirm('Are you sure you want to delete this user?')) {
            const token = localStorage.getItem('accessToken');
            try {
                const config = { headers: { Authorization: `Bearer ${token}` } };
                await axios.delete(`${API_URL}/admin/users/${userId}`, config);
                fetchUsers(); // Refresh the user list
            } catch (error) {
                alert('Failed to delete user.');
            }
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('accessToken');
        navigate('/login');
    };

    if (loading) return <p>Loading users...</p>;

    return (
        <div>
            <div className="d-flex justify-content-between align-items-center mb-4">
                <h2>Admin Dashboard: All Users</h2>
                <button onClick={handleLogout} className="btn btn-danger">Log Out</button>
            </div>
            <table className="table table-striped">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Course</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {users.map(user => (
                        <tr key={user.id}>
                            <td>{user.id}</td>
                            <td>{user.name}</td>
                            <td>{user.email}</td>
                            <td>{user.course ? user.course.name : 'N/A'}</td>
                            <td>
                                <button onClick={() => handleDelete(user.id)} className="btn btn-sm btn-danger">Delete</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
export default AdminDashboard;