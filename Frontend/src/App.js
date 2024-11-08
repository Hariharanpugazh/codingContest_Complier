// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import CreateContest from './pages/CreateContest';
import ContestPage from './pages/ContestPage';
import AutoContest from './pages/AutoContest';
import SelectTestOption from './pages/SelectTestOption';
import FileUpload from './pages/FileUpload';
import ManualSelectUI from './pages/ManualSelectUI'

import ContestChallenges from './pages/ContestChallenges';



function App() {
  return (
    <Router>
      <Routes>
        {/* <Route path="/" element={<AutoContest></AutoContest>}/> */}
        <Route path="/" element={<CreateContest />} />
        <Route path="/SelectTestOption" element={<SelectTestOption />}/>
        <Route path="/FileUpload" element={<FileUpload />} />
        <Route path="/ManualSelectUI" element={<ManualSelectUI />} />
        <Route path="/AutoContest" element={<AutoContest />} />
        <Route path="/contest" element={<ContestPage />} />
      </Routes>
    </Router>
  );
}

export default App;
