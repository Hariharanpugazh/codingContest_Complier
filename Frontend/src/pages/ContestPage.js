import React, { useState, useEffect } from 'react';
import { Menu, X } from 'lucide-react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import TestCaseSelection from '../components/TestCaseSelection';
import ProblemDetails from '../components/ProblemDetails';
import ExampleTestCase from '../components/ExampleTestCase';
import CodeEditor from '../components/CodeEditor';
import Buttons from '../components/Buttons';
import TestcaseResults from '../components/TestcaseResults';

const ContestPage = () => {
  const { id } = useParams(); // Fetch contest ID from URL
  const [isSidebarOpen, setSidebarOpen] = useState(false);
  const [codeMap, setCodeMap] = useState({}); // Store code for each problem-language pair
  const [language, setLanguage] = useState('python');
  const [testResults, setTestResults] = useState(null);
  const [submitSummary, setSubmitSummary] = useState(null);
  const [selectedProblemId, setSelectedProblemId] = useState(1);
  const [questionsData, setQuestionsData] = useState(null);// State to store fetched JSON data

  useEffect(() => {
    // Fetch the JSON file when the component mounts or when selectedProblemId changes
    fetch('/json/questions.json')
      .then((response) => response.json())
      .then((data) => {
        console.log("Data fetched:", data);
        setQuestionsData(data.problems); // Set the 'problems' array from the JSON
      })
      .catch((error) => {
        console.error('Error fetching JSON data:', error);
      });
  }, []);

  const handleProblemSelect = (problemId) => {
    setSelectedProblemId(problemId);
    setSidebarOpen(false); // Close sidebar on selection on mobile
  };

  const handleLanguageChange = (newLanguage) => {
    setLanguage(newLanguage);
  };

  const handleCodeChange = (newCode) => {
    setCodeMap((prev) => ({
      ...prev,
      [selectedProblemId]: {
        ...prev[selectedProblemId],
        [language]: newCode,
      },
    }));
  };

  const getCurrentCode = () => {
    return codeMap[selectedProblemId]?.[language] || '';
  };

  const handleCompileAndRun = async () => {
    try {
      const response = await axios.post('http://localhost:8000/compile/', {
        user_code: getCurrentCode(),
        language: language,
        problem_id: selectedProblemId,
      });
      setTestResults(response.data.results);
      setSubmitSummary(null);
    } catch (error) {
      console.error('Error during compile and run:', error);
      alert('There was an error running your code. Please try again.');
    }
  };

  const handleSubmit = async () => {
    try {
      const problemId = selectedProblemId; // Use selectedProblemId from state
  
      // Find the relevant problem data from the fetched JSON
      const problemData = questionsData?.find((item) => item.id === problemId);
  
      if (!problemData) {
        console.error('Problem data not found for the given ID');
        alert('Problem data not found. Please try again.');
        return;
      }
  
      // Submit the code for evaluation first
      const submitResponse = await axios.post('http://localhost:8000/submit/', {
        user_code: getCurrentCode(),
        language: language,
        problem_id: problemId,
      });
  
      const results = submitResponse.data.results;
      // console.log(testResults.expected_output)
      const passedCount = results.filter((result) => result.status === 'Success').length;
      const failedCount = results.length - passedCount;
  
      setSubmitSummary({
        passed: passedCount,
        failed: failedCount > 0 ? failedCount : null,
      });
      setTestResults(null);
  
      // Save code to temp_submission collection after submission
      await axios.post('http://localhost:8000/save-temp-submission/', {
        user_code: getCurrentCode(),
        language: language,
        problem_id: problemId,
        user_id: id,
        problem_data: problemData,
        passed: submitSummary.passed,
        failed: submitSummary.failed,// Include the fetched problem data
      });
  
      console.log('Temporary submission saved successfully.');
    } catch (error) {
      console.error('Error during temporary save or submission:', error);
      alert('There was an error processing your request. Please try again.');
    }
  };
  

  const handlePublishClick = async () => {
    console.log(id)
    try {
      const response = await axios.post('http://localhost:8000/finish/', {
        user_id: id, // Send the contest ID to the backend
      });
      console.log('Publish response:', response.data); // Log the response
    } catch (error) {
      console.error('Error during publish:', error);
      alert('There was an error publishing the contest. Please try again.');
    }
  };

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar Toggle Button - Mobile */}
      <button
        onClick={() => setSidebarOpen(!isSidebarOpen)}
        className="fixed top-4 left-4 z-50 p-2 bg-white rounded-md shadow-md lg:hidden"
      >
        {isSidebarOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      {/* Sidebar */}
      <div
        className={`fixed inset-y-0 left-0 transform ${
          isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
        } lg:relative lg:translate-x-0 w-64 bg-white shadow-lg transition-transform duration-300 ease-in-out z-40`}
      >
        <div className="h-full overflow-y-auto p-4 pt-16 lg:pt-4">
          <h2 className="text-xl font-bold mb-4">Problems</h2>
          <TestCaseSelection
            selectedProblem={selectedProblemId}
            onSelectProblem={handleProblemSelect}
          />
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        <div className="container mx-auto p-4">
          {/* Publish Button */}
          <div className="flex justify-end mb-4">
            <button
              onClick={handlePublishClick}
              className="bg-red-500 text-white px-6 py-2 rounded-md shadow-md hover:bg-red-600"
            >
              Finish
            </button>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {/* Problem Details Section */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <ProblemDetails selectedProblemId={selectedProblemId} />
              <div className="mt-6">
                <ExampleTestCase />
              </div>
            </div>

            {/* Code Editor Section */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <CodeEditor
                language={language}
                setLanguage={(lang) => {
                  handleLanguageChange(lang);
                }}
                code={getCurrentCode()}
                setCode={handleCodeChange}
              />
              <div className="mt-4">
                <Buttons onCompile={handleCompileAndRun} onSubmit={handleSubmit} />
              </div>
            </div>
          </div>

          {/* Results Section */}
          <div className="mt-6 bg-white rounded-lg shadow-md p-6">
            {submitSummary ? (
              <div>
                <h2 className="text-2xl font-semibold mb-4">Submission Summary</h2>
                <div className="space-y-2">
                  <p className="text-green-600">Passed: {submitSummary.passed}</p>
                  {submitSummary.failed && (
                    <p className="text-red-600">Failed: {submitSummary.failed}</p>
                  )}
                </div>
              </div>
            ) : (
              <TestcaseResults results={testResults} />
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ContestPage;