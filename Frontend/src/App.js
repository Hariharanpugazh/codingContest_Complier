import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import CreateContest from './pages/CreateContest';
import ContestPage from './pages/ContestPage';
import AutoContest from './pages/AutoContest';
import SelectTestOption from './pages/SelectTestOption';
import FileUpload from './pages/FileUpload';
import ManualSelectUI from './pages/ManualSelectUI'
import HrUpload from './pages/HrUploadPage';
import OnebyOne from './pages/OnebyOne'; // Adjust the import path as necessary





function App() {
  return (
    <Router>
      <Routes>
        {/* <Route path="/" element={<AutoContest></AutoContest>}/> */}
        {/* hr-page */}
        <Route path="/" element={<CreateContest />} />
        <Route path="/SelectTestOption" element={<SelectTestOption />}/>
        <Route path="/FileUpload" element={<FileUpload />} />
        <Route path="/ManualSelectUI" element={<ManualSelectUI />} />
        <Route path="/HrUpload" element={<HrUpload />}/>
        {/* user page */}
        <Route path="/OnebyOne" element={<OnebyOne />} /> {/* Add this route */}
        <Route path="/AutoContest" element={<AutoContest />} />
        <Route path="/contest" element={<ContestPage />} />
      </Routes>
    </Router>
  );
}

export default App;