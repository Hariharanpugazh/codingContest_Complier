import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Papa from 'papaparse';

function ContestChallenges() {
  const navigate = useNavigate();
  const [defaultChallenges, setDefaultChallenges] = useState([]);
  const [selectedChallenges, setSelectedChallenges] = useState([]);
  const [uploadedChallenges, setUploadedChallenges] = useState([]);

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

  // Handle CSV file upload
  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      Papa.parse(file, {
        header: true,
        complete: (results) => {
          setUploadedChallenges(results.data);
        },
        error: (error) => console.error('Error parsing CSV:', error),
      });
    }
  };

  // Placeholder function for Publish action
  const handlePublish = () => {
    alert('Published Successfully!');
    // Add any other logic for publishing here
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Contest Challenges</h1>

      {/* List of Default Challenges with Checkboxes */}
      <div className="mb-6">
        <h2 className="text-2xl font-semibold text-green-600">Select Default Challenges</h2>
        <p className="text-gray-600 mb-2">Choose challenges from our existing library.</p>
        <div className="border p-4 rounded-lg bg-white">
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

      {/* Display Selected Challenges */}
      {selectedChallenges.length > 0 && (
        <div className="mb-6">
          <h2 className="text-2xl font-semibold text-green-600">Selected Challenges</h2>
          <div className="border p-4 rounded-lg bg-white">
            <ul>
              {selectedChallenges.map((challenge) => (
                <li key={challenge.id} className="mb-2">
                  {challenge.title}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* CSV Upload */}
      <div className="mb-6">
        <h2 className="text-2xl font-semibold text-green-600">Upload Custom Challenges (CSV)</h2>
        <input
          type="file"
          accept=".csv"
          onChange={handleFileUpload}
          className="mt-2 border p-2 rounded bg-white"
        />
      </div>

      {/* Preview and Publish Buttons */}
      <div className="mt-6 flex gap-4">
        <button onClick={handlePreview} className="bg-green-600 text-white px-4 py-2 rounded">
          Preview
        </button>
        <button onClick={handlePublish} className="bg-green-600 text-white px-4 py-2 rounded">
          Publish
        </button>
      </div>
    </div>
  );
}

export default ContestChallenges;