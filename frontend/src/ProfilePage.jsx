import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_URL = 'https://tukur-student-matcher-project.onrender.com'

function ProfilePage() {
    const [user, setUser] = useState(null);
    const [courses, setCourses] = useState([]);
    const [interests, setInterests] = useState([]);
    const [selectedInterests, setSelectedInterests] = useState(new Set());
    const [selectedCourse, setSelectedCourse] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const fetchData = async () => {
            const token = localStorage.getItem('accessToken');
            if (!token) { navigate('/login'); return; }
            try {
                const config = { headers: { Authorization: `Bearer ${token}` } };
                const userRes = await axios.get(`${API_URL}/users/me`, config);
                const coursesRes = await axios.get(`${API_URL}/courses`);
                const interestsRes = await axios.get(`${API_URL}/interests`);

                setUser(userRes.data);
                setCourses(coursesRes.data);
                setInterests(interestsRes.data);
                setSelectedCourse(userRes.data.course.id);
                setSelectedInterests(new Set(userRes.data.interests.map(i => i.id)));
            } catch (err) {
                setError('Could not load profile data.');
            }
            setLoading(false);
        };
        fetchData();
    }, [navigate]);

    const handleInterestChange = (interestId) => {
        const newSelected = new Set(selectedInterests);
        if (newSelected.has(interestId)) {
            newSelected.delete(interestId);
        } else {
            newSelected.add(interestId);
        }
        setSelectedInterests(newSelected);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');
        const token = localStorage.getItem('accessToken');
        const updateData = {
            course_id: parseInt(selectedCourse),
            interest_ids: Array.from(selectedInterests),
        };
        try {
            const config = { headers: { Authorization: `Bearer ${token}` } };
            await axios.put(`${API_URL}/users/me`, updateData, config);
            setSuccess('Profile updated successfully!');
        } catch (err) {
            setError('Failed to update profile.');
        }
    };

    if (loading) return <p>Loading profile...</p>;

    return (
      <div className="card shadow-sm">
        <div className="card-body">
            <h3>Edit Your Profile</h3>
            <p>Welcome, {user.name}!</p>
            <form onSubmit={handleSubmit}>
                {error && <div className="alert alert-danger">{error}</div>}
                {success && <div className="alert alert-success">{success}</div>}
                 <div className="mb-3">
                    <label className="form-label">Course of Study</label>
                    <select className="form-select" value={selectedCourse} onChange={(e) => setSelectedCourse(e.target.value)} required>
                        {courses.map(course => (
                            <option key={course.id} value={course.id}>{course.name}</option>
                        ))}
                    </select>
                </div>
                <div className="mb-3">
                    <label className="form-label">Interests</label>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                        {interests.map(interest => (
                            <div key={interest.id} className="form-check">
                                <input className="form-check-input" type="checkbox" id={`interest-${interest.id}`} onChange={() => handleInterestChange(interest.id)} checked={selectedInterests.has(interest.id)}/>
                                <label className="form-check-label" htmlFor={`interest-${interest.id}`}>{interest.name}</label>
                            </div>
                        ))}
                    </div>
                </div>
                <button type="submit" className="btn btn-primary">Save Changes</button>
            </form>
        </div>
      </div>
    );
}

export default ProfilePage;