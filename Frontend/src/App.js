import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import CreateContest from './pages/CreateContest';
import ContestPage from './pages/ContestPage';
import StartContest from './pages/StartContest';
import SelectTestOption from './pages/SelectTestOption';
import FileUpload from './pages/FileUpload';
import ManualSelectUI from './pages/ManualSelectUI';
import HrUpload from './pages/HrUploadPage';
import OnebyOne from './pages/OnebyOne';
import ManualPage from './pages/ManualPage'; // Import ManualPage

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<CreateContest />} />
        <Route path="/SelectTestOption" element={<SelectTestOption />} />
        <Route path="/FileUpload" element={<FileUpload />} />
        <Route path="/ManualSelectUI" element={<ManualSelectUI />} />
        <Route path="/HrUpload/:contestId" element={<HrUpload />} />
        <Route path="/OnebyOne" element={<OnebyOne />} />
        <Route path="/StartContest" element={<StartContest />} />
        <Route path="/contest" element={<ContestPage />} />
        <Route path="/ManualPage/:contestId" element={<ManualPage />} /> {/* Add ManualPage route */}
      </Routes>
    </Router>
  );
}

export default App;