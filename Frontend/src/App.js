// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import CreateContest from './pages/CreateContest';
import ContestChallenges from './pages/ContestChallenges';
import ContestPage from './pages/ContestPage';
import AutoContest from './pages/AutoContest';

function App() {
  return (
    <Router>
      <Routes>
        {/* <Route path="/" element={<AutoContest></AutoContest>}/> */}
        <Route path="/" element={<CreateContest />} />
        <Route path="/AutoContest" element={<AutoContest />} />
        <Route path="/contest" element={<ContestPage />} />
      </Routes>
    </Router>
  );
}

export default App;
