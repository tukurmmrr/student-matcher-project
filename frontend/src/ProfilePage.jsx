import React, { useState, useEffect } from 'react';
import Select from 'react-select';
import axios from 'axios';

const ProfilePage = () => {
    const [selectedCourse, setSelectedCourse] = useState(null);
    const [selectedInterests, setSelectedInterests] = useState([]);
    const [courseOptions, setCourseOptions] = useState([]);
    const [interestOptions, setInterestOptions] = useState([]);
    const [isUpdating, setIsUpdating] = useState(false);
    const [message, setMessage] = useState('');

    useEffect(() => {
        const initializeProfile = async () => {
            try {
                // Load all available options
                const [coursesRes, interestsRes, profileRes] = await Promise.all([
                    axios.get('/courses'),
                    axios.get('/interests'),
                    axios.get('/users/me')
                ]);

                // Set dropdown options
                const courses = coursesRes.data.map(c => ({ value: c.id, label: c.name }));
                const interests = interestsRes.data.map(i => ({ value: i.id, label: i.name }));
                setCourseOptions(courses);
                setInterestOptions(interests);

                // Set current user selections
                const userProfile = profileRes.data;
                setSelectedCourse({
                    value: userProfile.course_id,
                    label: userProfile.course.name
                });

                const userInterests = userProfile.interests.map(i => ({
                    value: i.id,
                    label: i.name
                }));
                setSelectedInterests(userInterests);

            } catch (error) {
                console.error('Error loading profile:', error);
                setMessage('Failed to load profile data. Please refresh and try again.');
            }
        };

        initializeProfile();
    }, []);

    const saveProfileChanges = async (e) => {
        e.preventDefault();
        setIsUpdating(true);
        setMessage('');

        try {
            const updatedProfile = {
                course_id: selectedCourse.value,
                interest_ids: selectedInterests.map(interest => interest.value)
            };

            await axios.patch('/profile', updatedProfile);
            setMessage('✅ Profile updated successfully!');

            // Clear success message after a few seconds
            setTimeout(() => setMessage(''), 3000);

        } catch (error) {
            console.error('Profile update failed:', error);
            const errorText = error.response?.data?.detail || 'Something went wrong while updating your profile.';
            setMessage(`❌ Error: ${errorText}`);
        } finally {
            setIsUpdating(false);
        }
    };

    return (
        <div className="container">
            <div className="row justify-content-center">
                <div className="col-md-8">
                    <h2 className="mb-4">Edit Your Profile</h2>

                    {message && (
                        <div className={`alert ${message.includes('successfully') ? 'alert-success' : 'alert-danger'}`}>
                            {message}
                        </div>
                    )}

                    <form onSubmit={saveProfileChanges}>
                        <div className="mb-4">
                            <label className="form-label">Your Course</label>
                            <Select
                                options={courseOptions}
                                value={selectedCourse}
                                onChange={setSelectedCourse}
                                placeholder="Select your course"
                                isDisabled={isUpdating}
                            />
                        </div>

                        <div className="mb-4">
                            <label className="form-label">Your Interests</label>
                            <Select
                                options={interestOptions}
                                isMulti
                                value={selectedInterests}
                                onChange={setSelectedInterests}
                                placeholder="Choose your interests"
                                isDisabled={isUpdating}
                            />
                        </div>

                        <button
                            type="submit"
                            className="btn btn-primary"
                            disabled={isUpdating || !selectedCourse}
                        >
                            {isUpdating ? 'Updating...' : 'Save Changes'}
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default ProfilePage;