// src/components/ProblemDetails.js
import React, { useEffect, useState } from 'react';

function ProblemDetails({ selectedProblemId }) {
  const [problem, setProblem] = useState(null);

  // Load JSON data and find the selected problem
  useEffect(() => {
    fetch('/json/questions.json')
      .then((response) => response.json())
      .then((data) => {
        const selectedProblem = data.problems.find(
          (problem) => problem.id === parseInt(selectedProblemId)
          
        );
        console.log("geted")
        setProblem(selectedProblem);
        console.log(setProblem(selectedProblem))
      })
      .catch((error) => console.error("Error loading JSON:", error));
  }, [selectedProblemId]);

  if (!problem) return <div>Loading...</div>;

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
