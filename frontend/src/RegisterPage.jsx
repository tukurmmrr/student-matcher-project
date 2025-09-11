import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Select from 'react-select';
import axios from 'axios';

const RegisterPage = () => {
    const [currentStep, setCurrentStep] = useState(1);
    const [userInfo, setUserInfo] = useState({
        name: '',
        email: '',
        password: ''
    });

    // Options for dropdowns
    const [availableCourses, setAvailableCourses] = useState([]);
    const [availableInterests, setAvailableInterests] = useState([]);

    // User selections
    const [chosenCourse, setChosenCourse] = useState(null);
    const [chosenInterests, setChosenInterests] = useState([]);
    const [isLoading, setIsLoading] = useState(false);

    const navigate = useNavigate();

    // Load courses and interests when component mounts
    useEffect(() => {
        const loadOptions = async () => {
            try {
                const [coursesResponse, interestsResponse] = await Promise.all([
                    axios.get('/courses'),
                    axios.get('/interests')
                ]);

                // Transform data for react-select
                const courseOptions = coursesResponse.data.map(course => ({
                    value: course.id,
                    label: course.name
                }));

                const interestOptions = interestsResponse.data.map(interest => ({
                    value: interest.id,
                    label: interest.name
                }));

                setAvailableCourses(courseOptions);
                setAvailableInterests(interestOptions);
            } catch (error) {
                console.error('Failed to load options:', error);
            }
        };

        loadOptions();
    }, []);

    const proceedToNextStep = (e) => {
        e.preventDefault();
        setCurrentStep(2);
    };

    const updateUserInfo = (field, value) => {
        setUserInfo(prev => ({ ...prev, [field]: value }));
    };

    const completeRegistration = async (e) => {
        e.preventDefault();
        setIsLoading(true);

        try {
            const registrationData = {
                name: userInfo.name,
                email: userInfo.email,
                password: userInfo.password,
                course_id: chosenCourse.value,
                interest_ids: chosenInterests.map(interest => interest.value)
            };

            await axios.post('/register', registrationData);
            navigate('/login');
        } catch (error) {
            console.error('Registration failed:', error);
            const errorMsg = error.response?.data?.detail || 'Registration failed. Please try again.';
            alert(errorMsg); // TODO: Replace with proper error UI
        } finally {
            setIsLoading(false);
        }
    };

    // First step: basic info
    if (currentStep === 1) {
        return (
            <div className="container">
                <h2>Create Your Account</h2>
                <form onSubmit={proceedToNextStep}>
                    <div className="mb-3">
                        <input
                            type="text"
                            className="form-control"
                            placeholder="Your full name"
                            value={userInfo.name}
                            onChange={(e) => updateUserInfo('name', e.target.value)}
                            required
                        />
                    </div>

                    <div className="mb-3">
                        <input
                            type="email"
                            className="form-control"
                            placeholder="Email address"
                            value={userInfo.email}
                            onChange={(e) => updateUserInfo('email', e.target.value)}
                            required
                        />
                    </div>

                    <div className="mb-3">
                        <input
                            type="password"
                            className="form-control"
                            placeholder="Choose a password"
                            value={userInfo.password}
                            onChange={(e) => updateUserInfo('password', e.target.value)}
                            required
                        />
                    </div>

                    <button type="submit" className="btn btn-primary">
                        Continue →
                    </button>
                </form>
            </div>
        );
    }

    // Second step: course and interests
    return (
        <div className="container">
            <h2>Tell Us About Your Interests</h2>
            <form onSubmit={completeRegistration}>
                <div className="mb-4">
                    <label className="form-label">What course are you studying?</label>
                    <Select
                        options={availableCourses}
                        value={chosenCourse}
                        onChange={setChosenCourse}
                        placeholder="Choose your course"
                        isRequired
                    />
                </div>

                <div className="mb-4">
                    <label className="form-label">What are your interests? (Select multiple)</label>
                    <Select
                        options={availableInterests}
                        isMulti
                        value={chosenInterests}
                        onChange={setChosenInterests}
                        placeholder="Select your interests"
                    />
                </div>

                <button
                    type="submit"
                    className="btn btn-success"
                    disabled={isLoading || !chosenCourse}
                >
                    {isLoading ? 'Creating Account...' : 'Complete Registration'}
                </button>
            </form>
        </div>
    );
};

export default RegisterPage;