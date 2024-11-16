import React, { useEffect, useState } from 'react';

function ProblemDetails({ selectedProblemId }) {
  const [problem, setProblem] = useState(null);

  useEffect(() => {
    // Fetch the JSON file when the component mounts or when selectedProblemId changes
    fetch('/json/questions.json')
      .then((response) => response.json())
      .then((data) => {
        console.log("Data fetched:", data);

        const idToFind = parseInt(selectedProblemId, 10); // Convert to integer
        const selectedProblem = data.problems.find(
          (problem) => problem.id === idToFind
        );

        if (selectedProblem) {
          setProblem(selectedProblem); // Set the found problem
        } else {
          console.warn(`Problem with ID ${idToFind} not found. Defaulting to first problem.`);
          setProblem(data.problems[0]); // Default to the first problem if not found
        }
      })
      .catch((error) => {
        console.error("Error loading JSON:", error);
        // Handle errors if needed, like showing an error message
      });
  }, [selectedProblemId]); // Re-run the effect when selectedProblemId changes

  if (!problem) return <div>Loading...</div>; // Loading state while problem is being fetched

  return (
    <div className="mb-4">
      <h2 className="text-2xl font-semibold">{problem.title}</h2>
      <p className="mt-2 p-4 border rounded bg-gray-100">{problem.problem_statement}</p>

      <h3 className="text-lg font-semibold mt-4">Example Test Cases</h3>
      <ul className="list-disc ml-6">
        {problem.samples.map((sample, index) => (
          <li key={index}>
            <p>Input: {JSON.stringify(sample.input)}</p>
            <p>Expected Output: {sample.output}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ProblemDetails;
