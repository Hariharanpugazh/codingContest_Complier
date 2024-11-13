import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function CreateProfile() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    name: '',
    role: '',
    skills: [],
    contest_id: '' // New state for contest ID
  });
  
  const roles = ['Junior Software Developer', 'Senior Software Developer', 'AI Developer'];
  const skillsOptions = ['JavaScript', 'Python', 'React', 'Django', 'SQL', 'Java', 'Machine Learning', 'Cybersecurity'];

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSkillsChange = (e) => {
    const { options } = e.target;
    const selectedSkills = [];
    for (const option of options) {
      if (option.selected) {
        selectedSkills.push(option.value);
      }
    }
    setFormData({
      ...formData,
      skills: selectedSkills
    });
  };

  const handleSubmit = async () => {
    try {
      // Save contest data
      const contestResponse = await axios.post('http://localhost:8000/autocontest/', {
        role: formData.role,
        contest_id: formData.contest_id,  // Include contest_id in the request
      });
  
      console.log('Contest API response:', contestResponse.data);
      
      // Save user information in User_info collection
      const userResponse = await axios.post('http://localhost:8000/userinfo/', {
        name: formData.name,
        role: formData.role,
        skills: formData.skills,
        contest_id: formData.contest_id
      });
  
      console.log('User info API response:', userResponse.data);
      alert('Test started and user information saved successfully!');
      navigate('/Contest');
    } 
    catch (error) {
      console.error('Error starting test or saving user information:', error);
      alert('There was an error starting the test or saving user information. Please try again.');
    }
  };
  

  return (
    <div className="container mx-auto p-6 max-w-md">
      <div className="bg-white shadow-lg p-8 rounded-lg transition hover:shadow-xl">
        <h1 className="text-3xl font-semibold text-gray-700 mb-4">Create Profile</h1>
        <p className="text-gray-500 mb-6">Enter your details to start the test.</p>

        <div className="mb-4">
          <label className="block font-semibold text-gray-600 mb-2">Name <span className="text-red-500">*</span></label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleInputChange}
            required
            className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-400 focus:outline-none"
            placeholder="Enter your name"
          />
        </div>

        <div className="mb-4">
          <label className="block font-semibold text-gray-600 mb-2">Role <span className="text-red-500">*</span></label>
          <select
            name="role"
            value={formData.role}
            onChange={handleInputChange}
            required
            className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-400 focus:outline-none"
          >
            <option value="">Select a role</option>
            {roles.map((role, index) => (
              <option key={index} value={role}>{role}</option>
            ))}
          </select>
        </div>

        <div className="mb-4">
          <label className="block font-semibold text-gray-600 mb-2">Skills <span className="text-red-500">*</span></label>
          <select
            name="skills"
            multiple
            value={formData.skills}
            onChange={handleSkillsChange}
            className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-400 focus:outline-none"
          >
            {skillsOptions.map((skill, index) => (
              <option key={index} value={skill}>{skill}</option>
            ))}
          </select>
          <p className="text-sm text-gray-500 mt-2">Hold down the Ctrl (Windows) or Command (Mac) button to select multiple options.</p>
        </div>

        <div className="mb-6">
          <label className="block font-semibold text-gray-600 mb-2">Contest ID <span className="text-red-500">*</span></label>
          <input
            type="text"
            name="contest_id"
            value={formData.contest_id}
            onChange={handleInputChange}
            required
            className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-400 focus:outline-none"
            placeholder="Enter Contest ID"
          />
        </div>

        <button
          onClick={handleSubmit}
          className="w-full bg-gradient-to-r from-blue-500 to-blue-600 text-white py-3 rounded-lg font-semibold text-lg shadow-lg hover:shadow-xl transition duration-300 ease-in-out"
        >
          Start Test
        </button>
      </div>
    </div>
  );
}

export default CreateProfile;
