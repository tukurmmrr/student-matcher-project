import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Select from 'react-select';
import axios from 'axios';

const RegisterPage = () => {
    const [step, setStep] = useState(1);
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [courses, setCourses] = useState([]);
    const [selectedCourse, setSelectedCourse] = useState(null);
    const [interests, setInterests] = useState([]);
    const [selectedInterests, setSelectedInterests] = useState([]);

    const navigate = useNavigate();

    useEffect(() => {
        axios.get('/courses').then(res => setCourses(res.data.map(c => ({ value: c.id, label: c.name }))));
        axios.get('/interests').then(res => setInterests(res.data.map(i => ({ value: i.id, label: i.name }))));
    }, []);

    const handleStep1Submit = (e) => {
        e.preventDefault();
        setStep(2);
    };

    const handleStep2Submit = (e) => {
        e.preventDefault();
        const data = {
            name, email, password,
            course_id: selectedCourse.value,
            interest_ids: selectedInterests.map(i => i.value)
        };
        axios.post('/register', data).then(() => navigate('/login')).catch(err => alert(err.response.data.detail));
    };

    return (
        <div className="container">
            {step === 1 ? (
                <form onSubmit={handleStep1Submit}>
                    <input type="text" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} required />
                    <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
                    <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                    <button type="submit">Next</button>
                </form>
            ) : (
                <form onSubmit={handleStep2Submit}>
                    <Select options={courses} value={selectedCourse} onChange={setSelectedCourse} placeholder="Select Course" />
                    <Select options={interests} isMulti value={selectedInterests} onChange={setSelectedInterests} placeholder="Select Interests" />
                    <button type="submit">Register</button>
                </form>
            )}
        </div>
    );
};

export default RegisterPage;
