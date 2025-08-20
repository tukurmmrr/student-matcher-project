import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AdminDashboard = () => {
    const [users, setUsers] = useState([]);
    const [matchesJaccard, setMatchesJaccard] = useState([]);
    const [matchesDice, setMatchesDice] = useState([]);

    useEffect(() => {
        axios.get('/admin/users').then(res => setUsers(res.data)).catch(err => console.error(err));
        axios.get('/admin/matches/jaccard').then(res => setMatchesJaccard(res.data)).catch(err => console.error(err));
        axios.get('/admin/matches/dice').then(res => setMatchesDice(res.data)).catch(err => console.error(err));
    }, []);

    const handleDelete = (studentId) => {
        axios.delete(`/admin/users/${studentId}`).then(() => {
            setUsers(users.filter(u => u.id !== studentId));
            alert('User deleted successfully');
        }).catch(err => alert('Error deleting user: ' + err.response.data.detail));
    };

    const handleMakeAdmin = (studentId) => {
        axios.post(`/admin/make_admin/${studentId}`).then(res => {
            setUsers(users.map(u => u.id === studentId ? res.data : u));
            alert('User promoted to admin');
        }).catch(err => alert('Error promoting user: ' + err.response.data.detail));
    };

    return (
        <div class="container">
            <h2>Users</h2>
            <table class="table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {users.map(user => (
                        <tr key={user.id}>
                            <td>{user.name}</td>
                            <td>{user.email}</td>
                            <td>
                                <button onClick={() => handleDelete(user.id)}>Delete</button>
                                {!user.is_admin && <button onClick={() => handleMakeAdmin(user.id)}>Make Admin</button>}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>

            <h2>Jaccard Matches</h2>
            <ul>
                {matchesJaccard.map((match, index) => (
                    <li key={index}>{match.user1.name} ({match.user1.course.name}) matched with {match.user2.name} ({match.user2.course.name}) with score {match.score.toFixed(2)}</li>
                ))}
            </ul>

            <h2>Dice Matches</h2>
            <ul>
                {matchesDice.map((match, index) => (
                    <li key={index}>{match.user1.name} ({match.user1.course.name}) matched with {match.user2.name} ({match.user2.course.name}) with score {match.score.toFixed(2)}</li>
                ))}
            </ul>
        </div>
    );
};

export default AdminDashboard;
