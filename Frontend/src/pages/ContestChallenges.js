// src/pages/ContestChallenges.js
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

function ContestChallenges() {
  const navigate = useNavigate();
  const [defaultChallenges, setDefaultChallenges] = useState([]);
  const [selectedChallenges, setSelectedChallenges] = useState([]);

  // Load default challenges from JSON file
  useEffect(() => {
    fetch('/json/questions.json')
      .then((response) => response.json())
      .then((data) => setDefaultChallenges(data.problems))
      .catch((error) => console.error('Error loading JSON:', error));
  }, []);

  // Toggle selection of a challenge
  const handleChallengeSelect = (challenge) => {
    if (selectedChallenges.includes(challenge)) {
      setSelectedChallenges(selectedChallenges.filter((c) => c.id !== challenge.id));
    } else {
      setSelectedChallenges([...selectedChallenges, challenge]);
    }
  };

  // Preview selected problems on ContestPage
  const handlePreview = () => {
    if (selectedChallenges.length === 0) {
      alert('Please select at least one problem to preview');
      return;
    }
    navigate('/contest', { state: { problems: selectedChallenges } });
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Contest Challenges</h1>

      {/* List of Default Challenges with Checkboxes */}
      <div className="mb-6">
        <h2 className="text-2xl font-semibold">Select Default Challenges</h2>
        <p className="text-gray-600 mb-2">Choose challenges from our existing library.</p>
        <div className="border p-4 rounded-lg">
          {defaultChallenges.length > 0 ? (
            <ul>
              {defaultChallenges.map((challenge) => (
                <li key={challenge.id} className="flex items-center mb-2">
                  <input
                    type="checkbox"
                    checked={selectedChallenges.some((c) => c.id === challenge.id)}
                    onChange={() => handleChallengeSelect(challenge)}
                    className="mr-2"
                  />
                  <span>{challenge.title}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p>Loading challenges...</p>
          )}
        </div>
      </div>

      {/* Preview Button */}
      <div className="mt-6">
        <button onClick={handlePreview} className="bg-gray-500 text-white px-4 py-2 rounded">
          Preview
        </button>
      </div>
    </div>
  );
}

export default ContestChallenges;
