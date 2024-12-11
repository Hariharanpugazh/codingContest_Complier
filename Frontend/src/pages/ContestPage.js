import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import { useParams, useNavigate } from "react-router-dom";
import TestCaseSelection from '../components/TestCaseSelection';
import ProblemDetails from '../components/ProblemDetails';
import ExampleTestCase from '../components/ExampleTestCase';
import CodeEditor from '../components/CodeEditor';
import Buttons from '../components/Buttons';
import TestcaseResults from '../components/TestcaseResults';

function ContestPage() {
  const { testId } = useParams(); // Get testId from URL parameters
  const [selectedProblemId, setSelectedProblemId] = useState(1);
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState("python");
  const [testResults, setTestResults] = useState(null);
  const [submitSummary, setSubmitSummary] = useState(null);

  const navigate = useNavigate(); // Initialize useNavigate

  const mediaStreamRef = useRef(null); // Create a ref for mediaStream

  useEffect(() => {
    let mediaStream = null;

    // Set default code structure based on the selected language
    const setDefaultCodeStructure = () => {
      let defaultCode = "";
      switch (language) {
        case "python":
          defaultCode = `def main():\n    # Write your code here\n    pass\n\nif __name__ == "__main__":\n    main()`;
          break;
        case "javascript":
          defaultCode = `function main() {\n    // Write your code here\n}\n\nmain();`;
          break;
        // Add more languages and their default structures as needed
        default:
          defaultCode = "// Start coding here";
      }
      setCode(defaultCode);
    };

    setDefaultCodeStructure();

    const goFullScreen = async () => {
      try {
        const docElm = document.documentElement;
        if (docElm.requestFullscreen) {
          await docElm.requestFullscreen();
        } else if (docElm.mozRequestFullScreen) {
          await docElm.mozRequestFullScreen();
        } else if (docElm.webkitRequestFullScreen) {
          await docElm.webkitRequestFullScreen();
        } else if (docElm.msRequestFullscreen) {
          await docElm.msRequestFullscreen();
        } else {
          console.warn("Fullscreen API is not supported in this browser.");
        }
      } catch (error) {
        console.error("Error entering fullscreen mode:", error);
      }
    };

    const requestMediaAccess = async () => {
      try {
        console.log("Requesting media access...");
        mediaStreamRef.current = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        console.log("Media stream obtained:", mediaStreamRef.current);
      } catch (error) {
        if (error.name === "NotAllowedError") {
          alert("Please allow access to camera and microphone to proceed.");
        } else if (error.name === "NotFoundError") {
          alert("No media devices found. Please connect a camera or microphone.");
        } else {
          console.error("Error accessing media devices:", error);
          alert(`An unexpected error occurred: ${error.message}.`);
        }
      }
    };

    // Trigger fullscreen and request media access
    goFullScreen();
    requestMediaAccess();

    return () => {
      // Cleanup: stop media tracks when component unmounts
      if (mediaStreamRef.current) {
        mediaStreamRef.current.getTracks().forEach((track) => track.stop());
        console.log("Media stream stopped.");
      }
    };
  }, [language, testId]);

  // Handle problem selection
  const handleProblemSelect = (problemId) => {
    setSelectedProblemId(problemId);
  };

  // Handle code change
  const handleCodeChange = (newCode) => {
    setCode(newCode);
  };

  // Compile & Run
  const handleCompileAndRun = async () => {
    try {
      const response = await axios.post("http://localhost:8000/compile/", {
        user_code: code,
        language: language,
        problem_id: selectedProblemId,
      });
      setTestResults(response.data.results);
      setSubmitSummary(null); // Clear submit summary when running compile
    } catch (error) {
      console.error("Error during compile and run:", error);
      alert("There was an error running your code. Please try again.");
    }
  };

  // Submit Code
  const handleSubmit = async () => {
    try {
      const response = await axios.post("http://localhost:8000/submit/", {
        user_code: code,
        language: language,
        problem_id: selectedProblemId,
      });

      console.log("API Response:", response.data); // Log the response

      const results = response.data.results;
      const passedCount = results.filter((result) => result.stdout.trim() === result.expected_output.trim()).length;
      const failedCount = results.length - passedCount;

      setSubmitSummary({
        passed: passedCount,
        failed: failedCount > 0 ? failedCount : null,
      });
      setTestResults(null); // Clear testResults when submitting
    } catch (error) {
      console.error("Error during submission:", error);
      alert("There was an error submitting your code. Please try again.");
    }
  };

  // Handle finish action
// Inside the handleFinish function
const handleFinish = async () => {
  try {
    // Log the test as "completed" via API
    const studentId = localStorage.getItem("studentId");
    await axios.post("http://localhost:8000/api/finish_test/", {
      contest_id: testId,
      student_id: studentId,
    });

    // Exit fullscreen mode
    if (document.fullscreenElement) {
      await document.exitFullscreen();
    }

    // Stop media tracks
    if (mediaStreamRef.current) {
      const tracks = mediaStreamRef.current.getTracks();
      tracks.forEach((track) => {
        console.log(`Stopping track: ${track.kind}`);
        track.stop();
      });
      console.log("All media tracks stopped.");
    }

    // Redirect to the dashboard
    navigate("/studentdashboard");
  } catch (error) {
    console.error("Error finishing test:", error);
    alert("An error occurred while finishing the test. Please try again.");
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
          <button
            className="bg-orange-500 text-white font-bold py-2 px-4 rounded mt-4"
            onClick={handleFinish}
          >
            Finish
          </button>
        </div>
      </div>

      {/* Section for test case results or submit summary */}
      <div className="mt-6">
        {submitSummary ? (
          <div className="bg-white shadow-md rounded-lg p-6">
            <h2 className="text-2xl font-semibold mb-4">Submission Summary</h2>
            <h3 className="text-lg font-semibold mb-2">Hidden Test Case Results</h3>
            <div className="flex justify-normal items-center">
              <p className="text-green-600 font-medium">Passed: {submitSummary.passed}</p>
              {submitSummary.failed && (
                <p className="text-red-600 font-medium ml-">Failed: {submitSummary.failed}</p>
              )}
            </div>
          </div>
        ) : (
          <TestcaseResults results={testResults} />
        )}
      </div>
    </div>
  );
}

export default ContestPage;
