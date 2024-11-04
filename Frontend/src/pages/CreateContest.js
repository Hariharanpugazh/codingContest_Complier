// src/pages/CreateContest.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function CreateContest() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    contestName: '',
    startDate: '',
    startTime: '',
    endDate: '',
    endTime: '',
    noEndTime: false,
    organizationType: '',
    organizationName: ''
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Perform any necessary form validation or data submission logic here

    // Redirect to Contest Challenges page after form submission
    navigate('/contest-challenges');
  };

  return (
    <div className="container mx-auto p-4 max-w-lg">
      <div className="bg-white shadow p-6 rounded-lg">
        <h1 className="text-3xl font-bold mb-4">Create Contest</h1>
        <p className="text-gray-600 mb-6">
          Host your own coding contest. Select from available challenges or create your own.
        </p>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block font-bold mb-2">Contest Name <span className="text-red-500">*</span></label>
            <input
              type="text"
              name="contestName"
              value={formData.contestName}
              onChange={handleChange}
              required
              className="w-full border p-2 rounded"
            />
          </div>

          <div className="mb-4">
            <label className="block font-bold mb-2">Start Time <span className="text-red-500">*</span></label>
            <div className="flex gap-4">
              <input
                type="date"
                name="startDate"
                value={formData.startDate}
                onChange={handleChange}
                required
                className="w-1/2 border p-2 rounded"
              />
              <input
                type="time"
                name="startTime"
                value={formData.startTime}
                onChange={handleChange}
                required
                className="w-1/2 border p-2 rounded"
              />
            </div>
          </div>

          <div className="mb-4">
            <label className="block font-bold mb-2">End Time <span className="text-red-500">*</span></label>
            <div className="flex gap-4">
              <input
                type="date"
                name="endDate"
                value={formData.endDate}
                onChange={handleChange}
                disabled={formData.noEndTime}
                className="w-1/2 border p-2 rounded"
              />
              <input
                type="time"
                name="endTime"
                value={formData.endTime}
                onChange={handleChange}
                disabled={formData.noEndTime}
                className="w-1/2 border p-2 rounded"
              />
            </div>
            <div className="mt-2">
              <label className="inline-flex items-center">
                <input
                  type="checkbox"
                  name="noEndTime"
                  checked={formData.noEndTime}
                  onChange={handleChange}
                  className="mr-2"
                />
                This contest has no end time.
              </label>
            </div>
          </div>

          <div className="mb-4">
            <label className="block font-bold mb-2">Organization Type <span className="text-red-500">*</span></label>
            <select
              name="organizationType"
              value={formData.organizationType}
              onChange={handleChange}
              required
              className="w-full border p-2 rounded"
            >
              <option value="">Select organization type</option>
              <option value="School">School</option>
              <option value="Company">Company</option>
              <option value="University">University</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div className="mb-4">
            <label className="block font-bold mb-2">Organization Name <span className="text-red-500">*</span></label>
            <input
              type="text"
              name="organizationName"
              value={formData.organizationName}
              onChange={handleChange}
              required
              className="w-full border p-2 rounded"
            />
          </div>

          <button type="submit" className="bg-green-500 text-white w-full p-2 rounded mt-4">
            Get Started
          </button>
        </form>
      </div>
    </div>
  );
}

export default CreateContest;
