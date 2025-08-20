import React, { useState, useEffect } from 'react';
import Select from 'react-select';
import axios from 'axios';

const ProfilePage = () => {
    const [course, setCourse] = useState(null);
    const [interests, setInterests] = useState([]);
    const [courses, setCourses] = useState([]);
    const [allInterests, setAllInterests] = useState([]);

    useEffect(() => {
        axios.get('/courses').then(res => setCourses(res.data.map(c => ({ value: c.id, label: c.name }))));
        axios.get('/interests').then(res => setAllInterests(res.data.map(i => ({ value: i.id, label: i.name }))));
        axios.get('/users/me').then(res => {
            setCourse({ value: res.data.course_id, label: res.data.course.name });
            setInterests(res.data.interests.map(i => ({ value: i.id, label: i.name })));
        }).catch(err => console.error(err));
    }, []);

    const handleSubmit = (e) => {
        e.preventDefault();
        const data = {
            course_id: course.value,
            interest_ids: interests.map(i => i.value)
        };
        axios.patch('/profile', data).then(() => alert('Profile updated successfully')).catch(err => alert('Error updating profile: ' + err.response.data.detail));
    };

    return (
        <div class="container">
            <h2>Edit Profile</h2>
            <form onSubmit={handleSubmit}>
                <Select options={courses} value={course} onChange={setCourse} placeholder="Select Course" />
                <Select options={allInterests} isMulti value={interests} onChange={setInterests} placeholder="Select Interests" />
                <button type="submit">Update</button>
            </form>
        </div>
    );
};

export default ProfilePage;
