import React, { useState } from 'react';
import TestCaseSelection from '../components/TestCaseSelection';
import ProblemDetails from '../components/ProblemDetails';
import ExampleTestCase from '../components/ExampleTestCase';
import CodeEditor from '../components/CodeEditor';
import Buttons from '../components/Buttons';
import TestcaseResults from '../components/TestcaseResults';
import axios from 'axios';

function ContestPage() {
  const [selectedProblemId, setSelectedProblemId] = useState(1); // Default to the first problem
  const [code, setCode] = useState(''); // Code from CodeEditor
  const [language, setLanguage] = useState('python'); // Example default language
  const [testResults, setTestResults] = useState(null); // Results from API call
  const [submitSummary, setSubmitSummary] = useState(null);

  // Handle problem selection
  const handleProblemSelect = (problemId) => {
    console.log("Received Problem ID in ContestPage:", problemId);
    setSelectedProblemId(problemId);
    setCode(''); // Clear the code editor when a new problem is selected
  };

  // Handle code change from CodeEditor
  const handleCodeChange = (newCode) => {
    setCode(newCode);
  };

  // Handle Compile & Run button click
  const handleCompileAndRun = async () => {
    try {
      const response = await axios.post('http://localhost:8000/compile/', {
        user_code: code,
        language: language,
        problem_id: selectedProblemId,
      });

      // Set the response data to testResults state to display in TestcaseResults
      setTestResults(response.data.results);
      setSubmitSummary(null); // Clear submit summary when running compile
    } catch (error) {
      console.error('Error during compile and run:', error);
      alert('There was an error running your code. Please try again.');
    }
  };

  // Handle Submit button click
  const handleSubmit = async () => {
    try {
      const response = await axios.post('http://localhost:8000/submit/', {
        user_code: code,
        language: language,
        problem_id: selectedProblemId,
      });

      const results = response.data.results;
      const passedCount = results.filter((result) => result.status === 'Success').length;
      const failedCount = results.length - passedCount;

      setSubmitSummary({
        passed: passedCount,
        failed: failedCount > 0 ? failedCount : null, // Only show failed count if there are any
      });
      setTestResults(null); // Clear testResults when submitting
    } catch (error) {
      console.error('Error during submission:', error);
      alert('There was an error submitting your code. Please try again.');
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Contest Page</h1>

      {/* Left section for problem details */}
      <div className="flex">
        <div className="w-1/2 p-4">
          <TestCaseSelection selectedProblem={selectedProblemId} onSelectProblem={handleProblemSelect} />
          <ProblemDetails selectedProblemId={selectedProblemId} />
          <ExampleTestCase />
        </div>

        {/* Right section for code editor and buttons */}
        <div className="w-1/2 p-4">
          <CodeEditor
            language={language}
            setLanguage={setLanguage}
            code={code}
            setCode={handleCodeChange}
          />
          <Buttons onCompile={handleCompileAndRun} onSubmit={handleSubmit} />
        </div>
      </div>

      {/* Section for test case results or submit summary */}
      <div className="mt-6">
        {submitSummary ? (
          <div>
            <h2 className="text-2xl font-semibold">Submission Summary</h2>
            <p>Passed: {submitSummary.passed}</p>
            {submitSummary.failed && <p>Failed: {submitSummary.failed}</p>}
          </div>
        ) : (
          <TestcaseResults results={testResults} />
        )}
      </div>
    </div>
  );
}

export default ContestPage;